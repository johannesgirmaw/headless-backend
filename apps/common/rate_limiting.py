"""
Rate limiting middleware and utilities for API endpoints.
"""

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.exceptions import Throttled
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
import time
import logging

logger = logging.getLogger(__name__)


class CustomRateThrottle(UserRateThrottle):
    """
    Custom rate throttle with enhanced logging and metrics.
    """

    def throttle_failure(self):
        """
        Called when a request is throttled.
        """
        logger.warning(f"Rate limit exceeded for user: {self.scope}")
        return super().throttle_failure()

    def get_cache_key(self, request, view):
        """
        Generate cache key for rate limiting.
        """
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return f"throttle_{self.scope}_{ident}"


class APIRateLimitMiddleware(MiddlewareMixin):
    """
    Middleware for API rate limiting.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_request(self, request):
        """
        Process request for rate limiting.
        """
        # Only apply to API endpoints
        if not request.path.startswith('/api/'):
            return None

        # Skip rate limiting for health checks
        if request.path.startswith('/health/') or request.path.startswith('/metrics/'):
            return None

        # Get rate limit settings
        rate_limit_enabled = getattr(settings, 'RATE_LIMIT_ENABLED', True)
        if not rate_limit_enabled:
            return None

        # Get user identifier
        if request.user and request.user.is_authenticated:
            user_id = request.user.pk
            rate_limit_key = f"rate_limit_user_{user_id}"
            max_requests = getattr(settings, 'RATE_LIMIT_PER_HOUR', 1000)
        else:
            # Use IP address for anonymous users
            ip_address = self.get_client_ip(request)
            rate_limit_key = f"rate_limit_ip_{ip_address}"
            max_requests = getattr(settings, 'RATE_LIMIT_PER_MINUTE', 100)

        # Check rate limit
        current_requests = cache.get(rate_limit_key, 0)

        if current_requests >= max_requests:
            logger.warning(
                f"Rate limit exceeded for {rate_limit_key}: {current_requests}/{max_requests}")
            return JsonResponse(
                {
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Limit: {max_requests} per hour',
                    'retry_after': 3600  # 1 hour
                },
                status=429
            )

        # Increment counter
        cache.set(rate_limit_key, current_requests + 1, 3600)  # 1 hour TTL

        return None

    def get_client_ip(self, request):
        """
        Get client IP address from request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AdvancedRateThrottle:
    """
    Advanced rate limiting with multiple strategies.
    """

    def __init__(self):
        self.cache = cache

    def check_rate_limit(self, identifier, limit_type='user', time_window=3600):
        """
        Check rate limit for a given identifier.

        Args:
            identifier: User ID or IP address
            limit_type: Type of limit ('user', 'ip', 'endpoint')
            time_window: Time window in seconds

        Returns:
            dict: Rate limit status
        """
        cache_key = f"rate_limit_{limit_type}_{identifier}"
        current_count = self.cache.get(cache_key, 0)

        # Get limit based on type
        if limit_type == 'user':
            max_requests = getattr(settings, 'RATE_LIMIT_PER_HOUR', 1000)
        elif limit_type == 'ip':
            max_requests = getattr(settings, 'RATE_LIMIT_PER_MINUTE', 100)
        else:
            max_requests = 100  # Default limit

        if current_count >= max_requests:
            return {
                'allowed': False,
                'current_count': current_count,
                'max_requests': max_requests,
                'retry_after': time_window,
                'reset_time': time.time() + time_window
            }

        # Increment counter
        self.cache.set(cache_key, current_count + 1, time_window)

        return {
            'allowed': True,
            'current_count': current_count + 1,
            'max_requests': max_requests,
            'retry_after': 0,
            'reset_time': time.time() + time_window
        }

    def get_rate_limit_status(self, identifier, limit_type='user'):
        """
        Get current rate limit status without incrementing.

        Args:
            identifier: User ID or IP address
            limit_type: Type of limit

        Returns:
            dict: Rate limit status
        """
        cache_key = f"rate_limit_{limit_type}_{identifier}"
        current_count = self.cache.get(cache_key, 0)

        if limit_type == 'user':
            max_requests = getattr(settings, 'RATE_LIMIT_PER_HOUR', 1000)
        elif limit_type == 'ip':
            max_requests = getattr(settings, 'RATE_LIMIT_PER_MINUTE', 100)
        else:
            max_requests = 100

        return {
            'current_count': current_count,
            'max_requests': max_requests,
            'remaining': max(0, max_requests - current_count),
            'reset_time': time.time() + 3600
        }


class EndpointRateThrottle:
    """
    Rate limiting for specific endpoints.
    """

    def __init__(self):
        self.cache = cache
        self.endpoint_limits = {
            # 5 requests per 5 minutes
            '/api/v1/auth/login/': {'limit': 5, 'window': 300},
            # 3 requests per hour
            '/api/v1/auth/register/': {'limit': 3, 'window': 3600},
            # 3 requests per hour
            '/api/v1/auth/forgot-password/': {'limit': 3, 'window': 3600},
            # 100 requests per hour
            '/api/v1/users/': {'limit': 100, 'window': 3600},
            # 50 requests per hour
            '/api/v1/accounts/': {'limit': 50, 'window': 3600},
        }

    def check_endpoint_rate_limit(self, request):
        """
        Check rate limit for specific endpoint.

        Args:
            request: Django request object

        Returns:
            dict: Rate limit status
        """
        endpoint = request.path
        if endpoint not in self.endpoint_limits:
            return {'allowed': True}

        limit_config = self.endpoint_limits[endpoint]
        limit = limit_config['limit']
        window = limit_config['window']

        # Create identifier based on user or IP
        if request.user and request.user.is_authenticated:
            identifier = f"user_{request.user.pk}"
        else:
            identifier = f"ip_{self.get_client_ip(request)}"

        cache_key = f"endpoint_rate_limit_{endpoint}_{identifier}"
        current_count = self.cache.get(cache_key, 0)

        if current_count >= limit:
            logger.warning(
                f"Endpoint rate limit exceeded for {endpoint}: {current_count}/{limit}")
            return {
                'allowed': False,
                'current_count': current_count,
                'max_requests': limit,
                'retry_after': window,
                'endpoint': endpoint
            }

        # Increment counter
        self.cache.set(cache_key, current_count + 1, window)

        return {
            'allowed': True,
            'current_count': current_count + 1,
            'max_requests': limit,
            'retry_after': 0,
            'endpoint': endpoint
        }

    def get_client_ip(self, request):
        """
        Get client IP address from request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


def rate_limit_decorator(limit_type='user', max_requests=100, time_window=3600):
    """
    Decorator for rate limiting views.

    Args:
        limit_type: Type of limit ('user', 'ip', 'endpoint')
        max_requests: Maximum number of requests
        time_window: Time window in seconds

    Returns:
        Decorated function
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Get identifier
            if limit_type == 'user' and request.user and request.user.is_authenticated:
                identifier = request.user.pk
            elif limit_type == 'ip':
                identifier = request.META.get('REMOTE_ADDR')
            else:
                identifier = request.path

            # Check rate limit
            throttle = AdvancedRateThrottle()
            rate_status = throttle.check_rate_limit(
                identifier, limit_type, time_window)

            if not rate_status['allowed']:
                return JsonResponse(
                    {
                        'error': 'Rate limit exceeded',
                        'message': f'Too many requests. Limit: {max_requests} per {time_window} seconds',
                        'retry_after': rate_status['retry_after']
                    },
                    status=429
                )

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
