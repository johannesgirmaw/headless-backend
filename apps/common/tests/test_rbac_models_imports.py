import pytest


def test_rbac_models_imports():
    from apps.common import rbac_models as rm

    # Ensure core RBAC models are present
    assert hasattr(rm, 'Permission')
    assert hasattr(rm, 'Role')
    assert hasattr(rm, 'RolePermission')
    assert hasattr(rm, 'UserRole')
    assert hasattr(rm, 'UserPermission')
    assert hasattr(rm, 'UserGroup')
    assert hasattr(rm, 'UserGroupMembership')
    assert hasattr(rm, 'RoleGroup')
