def test_rbac_permissions_classes_exist():
    from apps.common import rbac_permissions as rp

    assert hasattr(rp, 'RBACPermission')
    assert hasattr(rp, 'ModelRBACPermission')
    assert hasattr(rp, 'OrganizationPermission')
    assert hasattr(rp, 'AccountPermission')
    assert hasattr(rp, 'IsOwnerOrReadOnly')
    assert hasattr(rp, 'IsOwnerOrAdmin')
