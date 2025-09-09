import pytest


@pytest.mark.django_db
def test_team_member_list_requires_auth(client):
    resp = client.get('/api/v1/team-members/')
    assert resp.status_code in (401, 403)
