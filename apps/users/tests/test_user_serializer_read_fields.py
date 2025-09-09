import pytest
from django.contrib.auth import get_user_model
from apps.users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer_includes_computed_fields():
    User = get_user_model()
    user = User.objects.create_user(
        email='x@example.com', password='12345678', first_name='X', last_name='Y')
    data = UserSerializer(user).data
    for key in ['full_name', 'display_name', 'permissions', 'roles', 'groups']:
        assert key in data
