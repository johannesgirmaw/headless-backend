"""
Monitoring and logging utilities for the headless SaaS platform.
"""

import logging
import time
from functools import wraps
from django.core.cache import cache
from django.db import connection
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.base import ContentFile
import psutil
import os


class PerformanceMonitor:
    """
    Performance monitoring utilities.
    """

    @staticmethod
    def get_system_metrics():
        """
        Get system performance metrics.

        Returns:
            dict: System metrics
        """
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024 * 1024)  # MB
            memory_total = memory.total / (1024 * 1024)  # MB

            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used = disk.used / (1024 * 1024 * 1024)  # GB
            disk_total = disk.total / (1024 * 1024 * 1024)  # GB

            # Process info
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / (1024 * 1024)  # MB
            process_cpu = process.cpu_percent()

            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_used_mb': round(memory_used, 2),
                'memory_total_mb': round(memory_total, 2),
                'disk_percent': round(disk_percent, 2),
                'disk_used_gb': round(disk_used, 2),
                'disk_total_gb': round(disk_total, 2),
                'process_memory_mb': round(process_memory, 2),
                'process_cpu_percent': process_cpu,
            }

        except Exception as e:
            logging.error(f"Failed to get system metrics: {str(e)}")
            return {}

    @staticmethod
    def get_database_metrics():
        """
        Get database performance metrics.

        Returns:
            dict: Database metrics
        """
        try:
            with connection.cursor() as cursor:
                # Get connection count
                cursor.execute(
                    "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
                active_connections = cursor.fetchone()[0]

                # Get database size
                cursor.execute(
                    "SELECT pg_size_pretty(pg_database_size(current_database()))")
                db_size = cursor.fetchone()[0]

                # Get table sizes
                cursor.execute("""
                    SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
                    LIMIT 10
                """)
                table_sizes = cursor.fetchall()

                return {
                    'active_connections': active_connections,
                    'database_size': db_size,
                    'table_sizes': [
                        {'schema': row[0], 'table': row[1], 'size': row[2]}
                        for row in table_sizes
                    ]
                }

        except Exception as e:
            logging.error(f"Failed to get database metrics: {str(e)}")
            return {}

    @staticmethod
    def get_cache_metrics():
        """
        Get cache performance metrics.

        Returns:
            dict: Cache metrics
        """
        try:
            # Test cache connectivity
            test_key = 'health_check_test'
            test_value = 'test_value'

            # Set test value
            cache.set(test_key, test_value, 10)

            # Get test value
            retrieved_value = cache.get(test_key)

            # Delete test value
            cache.delete(test_key)

            # Get cache info if available
            cache_info = {}
            if hasattr(cache, 'get_stats'):
                cache_info = cache.get_stats()

            return {
                'connected': retrieved_value == test_value,
                'stats': cache_info,
            }

        except Exception as e:
            logging.error(f"Failed to get cache metrics: {str(e)}")
            return {'connected': False, 'error': str(e)}


def performance_monitor(func):
    """
    Decorator to monitor function performance.

    Args:
        func: Function to monitor

    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Log performance metrics
            logging.info(
                f"Function {func.__name__} executed in {execution_time:.3f}s")

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logging.error(
                f"Function {func.__name__} failed after {execution_time:.3f}s: {str(e)}")
            raise

    return wrapper


class HealthCheckView(View):
    """
    Health check endpoint for monitoring.
    """

    @method_decorator(require_http_methods(["GET"]))
    def get(self, request):
        """
        Perform health checks on various system components.

        Returns:
            JsonResponse: Health check results
        """
        health_status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'checks': {}
        }

        # Database health check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            health_status['checks']['database'] = {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
        except Exception as e:
            health_status['checks']['database'] = {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}'
            }
            health_status['status'] = 'unhealthy'

        # Cache health check
        try:
            test_key = 'health_check_cache'
            cache.set(test_key, 'test', 10)
            cache.get(test_key)
            cache.delete(test_key)
            health_status['checks']['cache'] = {
                'status': 'healthy',
                'message': 'Cache connection successful'
            }
        except Exception as e:
            health_status['checks']['cache'] = {
                'status': 'unhealthy',
                'message': f'Cache connection failed: {str(e)}'
            }
            health_status['status'] = 'unhealthy'

        # Storage health check
        try:
            from django.core.files.storage import default_storage
            test_file = 'health_check_test.txt'
            default_storage.save(test_file, ContentFile(b'test'))
            default_storage.exists(test_file)
            default_storage.delete(test_file)
            health_status['checks']['storage'] = {
                'status': 'healthy',
                'message': 'Storage connection successful'
            }
        except Exception as e:
            health_status['checks']['storage'] = {
                'status': 'unhealthy',
                'message': f'Storage connection failed: {str(e)}'
            }
            health_status['status'] = 'unhealthy'

        # System metrics
        try:
            monitor = PerformanceMonitor()
            system_metrics = monitor.get_system_metrics()
            health_status['checks']['system'] = {
                'status': 'healthy',
                'message': 'System metrics retrieved',
                'metrics': system_metrics
            }
        except Exception as e:
            health_status['checks']['system'] = {
                'status': 'unhealthy',
                'message': f'System metrics failed: {str(e)}'
            }

        # Determine overall status
        if health_status['status'] == 'healthy':
            return JsonResponse(health_status, status=200)
        else:
            return JsonResponse(health_status, status=503)


class MetricsView(View):
    """
    Metrics endpoint for monitoring.
    """

    @method_decorator(require_http_methods(["GET"]))
    def get(self, request):
        """
        Get system metrics.

        Returns:
            JsonResponse: System metrics
        """
        try:
            monitor = PerformanceMonitor()

            metrics = {
                'timestamp': time.time(),
                'system': monitor.get_system_metrics(),
                'database': monitor.get_database_metrics(),
                'cache': monitor.get_cache_metrics(),
            }

            return JsonResponse(metrics, status=200)

        except Exception as e:
            logging.error(f"Failed to get metrics: {str(e)}")
            return JsonResponse(
                {'error': 'Failed to retrieve metrics'},
                status=500
            )


class LoggingConfig:
    """
    Centralized logging configuration.
    """

    @staticmethod
    def setup_logging():
        """
        Setup logging configuration.
        """
        logging.basicConfig(
            level=getattr(settings, 'LOG_LEVEL', 'INFO'),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    getattr(settings, 'LOG_FILE', 'django.log')),
                logging.StreamHandler(),
            ]
        )

        # Set specific loggers
        logging.getLogger('django').setLevel(
            getattr(settings, 'LOG_LEVEL', 'INFO'))
        logging.getLogger('apps').setLevel(
            getattr(settings, 'LOG_LEVEL', 'INFO'))
        logging.getLogger('celery').setLevel(
            getattr(settings, 'LOG_LEVEL', 'INFO'))

        # Reduce noise from third-party libraries
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)
