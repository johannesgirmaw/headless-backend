import pytest


@pytest.mark.django_db
def test_account_stats_requires_auth(client):
    resp = client.get('/api/v1/accounts/stats/')
    assert resp.status_code in (401, 403)
