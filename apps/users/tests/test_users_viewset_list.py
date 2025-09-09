import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_users_list_requires_auth(client):
    url = '/api/v1/users/'
    resp = client.get(url)
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_users_list_authenticated(api_client):
    User = get_user_model()
    user = User.objects.create_user(
        email='u@example.com', password='pass123456', first_name='U', last_name='S')
    api_client.force_authenticate(user=user)
    url = '/api/v1/users/'
    resp = api_client.get(url)
    assert resp.status_code == 200
