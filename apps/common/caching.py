"""
Caching utilities and decorators for improved performance.
"""

from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json
import logging
import time

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Centralized cache management utilities.
    """

    DEFAULT_TTL = getattr(settings, 'CACHE_TTL', 300)  # 5 minutes
    MAX_TTL = 86400  # 24 hours

    @classmethod
    def generate_cache_key(cls, prefix, *args, **kwargs):
        """
        Generate a unique cache key from arguments.

        Args:
            prefix: Cache key prefix
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            str: Generated cache key
        """
        # Convert all arguments to strings and sort them
        key_parts = [str(arg) for arg in args]
        key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])

        # Create hash of the key parts
        key_string = ":".join(key_parts)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()

        return f"{prefix}:{key_hash}"

    @classmethod
    def get_or_set(cls, key, callable_func, timeout=None, *args, **kwargs):
        """
        Get value from cache or set it using callable.

        Args:
            key: Cache key
            callable_func: Function to call if cache miss
            timeout: Cache timeout in seconds
            *args: Arguments for callable function
            **kwargs: Keyword arguments for callable function

        Returns:
            Cached value or result of callable function
        """
        if timeout is None:
            timeout = cls.DEFAULT_TTL

        # Try to get from cache
        cached_value = cache.get(key)
        if cached_value is not None:
            logger.debug(f"Cache hit for key: {key}")
            return cached_value

        # Cache miss, call function and cache result
        logger.debug(f"Cache miss for key: {key}")
        result = callable_func(*args, **kwargs)

        # Cache the result
        cache.set(key, result, timeout)
        logger.debug(f"Cached result for key: {key}")

        return result

    @classmethod
    def invalidate_pattern(cls, pattern):
        """
        Invalidate all cache keys matching a pattern.

        Args:
            pattern: Cache key pattern to match

        Returns:
            int: Number of keys invalidated
        """
        try:
            # This is a simplified version - in production, you might want to use
            # a more sophisticated pattern matching system
            keys = cache.keys(f"*{pattern}*")
            if keys:
                cache.delete_many(keys)
                logger.info(
                    f"Invalidated {len(keys)} cache keys matching pattern: {pattern}")
                return len(keys)
            return 0
        except Exception as e:
            logger.error(
                f"Failed to invalidate cache pattern {pattern}: {str(e)}")
            return 0

    @classmethod
    def get_cache_stats(cls):
        """
        Get cache statistics.

        Returns:
            dict: Cache statistics
        """
        try:
            stats = {
                'backend': cache.__class__.__name__,
                'location': getattr(cache, '_cache', {}).get('location', 'unknown'),
            }

            # Try to get additional stats if available
            if hasattr(cache, 'get_stats'):
                stats.update(cache.get_stats())

            return stats
        except Exception as e:
            logger.error(f"Failed to get cache stats: {str(e)}")
            return {'error': str(e)}


def cache_result(timeout=None, key_prefix=None, key_func=None):
    """
    Decorator to cache function results.

    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache key
        key_func: Function to generate cache key

    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                prefix = key_prefix or func.__name__
                cache_key = CacheManager.generate_cache_key(
                    prefix, *args, **kwargs)

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result

            # Cache miss, execute function
            logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
            result = func(*args, **kwargs)

            # Cache the result
            cache.set(cache_key, result, timeout or CacheManager.DEFAULT_TTL)
            logger.debug(f"Cached result for {func.__name__}: {cache_key}")

            return result

        return wrapper
    return decorator


def cache_invalidate(pattern_func):
    """
    Decorator to invalidate cache after function execution.

    Args:
        pattern_func: Function that returns cache pattern to invalidate

    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function
            result = func(*args, **kwargs)

            # Invalidate cache
            try:
                pattern = pattern_func(*args, **kwargs)
                if pattern:
                    CacheManager.invalidate_pattern(pattern)
                    logger.info(f"Invalidated cache pattern: {pattern}")
            except Exception as e:
                logger.error(f"Failed to invalidate cache: {str(e)}")

            return result

        return wrapper
    return decorator


class ModelCacheMixin:
    """
    Mixin for model caching functionality.
    """

    @classmethod
    def get_cached(cls, pk, timeout=None):
        """
        Get model instance from cache.

        Args:
            pk: Primary key
            timeout: Cache timeout

        Returns:
            Model instance or None
        """
        cache_key = f"{cls.__name__}:{pk}"
        return cache.get(cache_key)

    @classmethod
    def set_cached(cls, instance, timeout=None):
        """
        Cache model instance.

        Args:
            instance: Model instance
            timeout: Cache timeout

        Returns:
            bool: Success status
        """
        cache_key = f"{cls.__name__}:{instance.pk}"
        cache.set(cache_key, instance, timeout or CacheManager.DEFAULT_TTL)
        return True

    @classmethod
    def invalidate_cached(cls, pk):
        """
        Invalidate cached model instance.

        Args:
            pk: Primary key

        Returns:
            bool: Success status
        """
        cache_key = f"{cls.__name__}:{pk}"
        cache.delete(cache_key)
        return True

    @classmethod
    def get_or_set_cached(cls, pk, timeout=None):
        """
        Get model instance from cache or database.

        Args:
            pk: Primary key
            timeout: Cache timeout

        Returns:
            Model instance
        """
        # Try cache first
        cached_instance = cls.get_cached(pk, timeout)
        if cached_instance is not None:
            return cached_instance

        # Get from database
        try:
            instance = cls.objects.get(pk=pk)
            cls.set_cached(instance, timeout)
            return instance
        except cls.DoesNotExist:
            return None


class QuerySetCache:
    """
    Cache for QuerySet results.
    """

    @staticmethod
    def cache_queryset(queryset, cache_key, timeout=None):
        """
        Cache QuerySet results.

        Args:
            queryset: Django QuerySet
            cache_key: Cache key
            timeout: Cache timeout

        Returns:
            Cached QuerySet results
        """
        if timeout is None:
            timeout = CacheManager.DEFAULT_TTL

        # Try to get from cache
        cached_results = cache.get(cache_key)
        if cached_results is not None:
            logger.debug(f"QuerySet cache hit: {cache_key}")
            return cached_results

        # Cache miss, evaluate QuerySet
        logger.debug(f"QuerySet cache miss: {cache_key}")
        results = list(queryset)

        # Cache the results
        cache.set(cache_key, results, timeout)
        logger.debug(f"Cached QuerySet results: {cache_key}")

        return results

    @staticmethod
    def invalidate_queryset_cache(pattern):
        """
        Invalidate QuerySet cache by pattern.

        Args:
            pattern: Cache pattern to invalidate

        Returns:
            int: Number of keys invalidated
        """
        return CacheManager.invalidate_pattern(f"queryset:{pattern}")


class CacheWarmer:
    """
    Utility for warming up cache with frequently accessed data.
    """

    @staticmethod
    def warm_user_cache():
        """
        Warm up user-related cache.
        """
        try:
            from apps.users.models import User

            # Cache active users
            active_users = User.objects.filter(is_active=True)
            cache_key = "active_users"
            cache.set(cache_key, list(active_users.values(
                'id', 'email', 'first_name', 'last_name')), 3600)

            logger.info("User cache warmed up successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to warm user cache: {str(e)}")
            return False

    @staticmethod
    def warm_account_cache():
        """
        Warm up account-related cache.
        """
        try:
            from apps.accounts.models import Account

            # Cache active accounts
            active_accounts = Account.objects.filter(is_active=True)
            cache_key = "active_accounts"
            cache.set(cache_key, list(active_accounts.values(
                'id', 'account_id', 'company_name')), 3600)

            logger.info("Account cache warmed up successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to warm account cache: {str(e)}")
            return False

    @staticmethod
    def warm_all_caches():
        """
        Warm up all caches.
        """
        results = {
            'user_cache': CacheWarmer.warm_user_cache(),
            'account_cache': CacheWarmer.warm_account_cache(),
        }

        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)

        logger.info(
            f"Cache warming completed: {success_count}/{total_count} successful")
        return results
