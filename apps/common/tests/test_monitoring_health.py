import pytest
from django.test import RequestFactory
from apps.common.monitoring import HealthCheckView


@pytest.mark.django_db
def test_health_check_returns_json_status_code():
    rf = RequestFactory()
    req = rf.get('/health/')
    res = HealthCheckView.as_view()(req)
    assert res.status_code in (200, 503)
    assert 'application/json' in res.get('Content-Type', '')
