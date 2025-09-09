import pytest
from django.contrib.auth import get_user_model
from apps.common.rbac_manager import get_rbac_manager


@pytest.mark.django_db
def test_rbac_manager_returns_set():
    User = get_user_model()
    user = User.objects.create_user(
        email='t@example.com', password='p@ssW0rd!', first_name='T', last_name='U')
    r = get_rbac_manager(user)
    perms = r.get_user_permissions()
    assert isinstance(perms, set)
