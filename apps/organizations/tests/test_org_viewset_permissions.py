import pytest


@pytest.mark.django_db
def test_org_list_requires_auth(client):
    resp = client.get('/api/v1/organizations/')
    assert resp.status_code in (401, 403)
