import pytest
from django.core.cache import cache
from apps.common.caching import CacheManager, cache_result


def test_cache_manager_generate_cache_key_is_stable():
    k1 = CacheManager.generate_cache_key('prefix', 1, a=2, b=3)
    k2 = CacheManager.generate_cache_key('prefix', 1, b=3, a=2)
    assert k1 == k2
    assert k1.startswith('prefix:')


def test_cache_result_decorator_caches(monkeypatch):
    calls = {'count': 0}

    @cache_result(timeout=5, key_prefix='t')
    def add(a, b):
        calls['count'] += 1
        return a + b

    cache.delete_many([k for k in cache.iter_keys('*')]
                      ) if hasattr(cache, 'iter_keys') else None

    assert add(2, 3) == 5
    assert add(2, 3) == 5
    assert calls['count'] == 1
