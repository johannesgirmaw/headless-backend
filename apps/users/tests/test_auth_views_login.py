import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_login_obtain_token(client):
    User = get_user_model()
    User.objects.create_user(
        email='jane@example.com', password='strongpass123', first_name='Jane', last_name='Doe'
    )

    url = reverse('token_obtain_pair')
    resp = client.post(
        url, data={'email': 'jane@example.com', 'password': 'strongpass123'})
    assert resp.status_code == 200
    body = resp.json()
    assert 'access' in body and 'refresh' in body
