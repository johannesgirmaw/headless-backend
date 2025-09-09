from apps.common.rate_limiting import CustomRateThrottle


def test_custom_rate_throttle_cache_key_for_anon(rf):
    throttle = CustomRateThrottle()
    req = rf.get('/api/v1/ping')
    key = throttle.get_cache_key(req, view=None)
    assert key.startswith('throttle_')
