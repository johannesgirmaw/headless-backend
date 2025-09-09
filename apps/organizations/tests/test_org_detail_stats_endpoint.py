import pytest


@pytest.mark.django_db
def test_org_stats_requires_auth(client):
    resp = client.get('/api/v1/organizations/stats/')
    assert resp.status_code in (401, 403)
