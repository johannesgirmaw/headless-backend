import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_user_generate_user_id_default_assigned():
    User = get_user_model()
    user = User.objects.create_user(
        email='john@example.com', password='password', first_name='John', last_name='Doe'
    )
    assert user.user_id.startswith('USR-')
    assert len(user.user_id) <= 32
