from apps.organizations.serializers import OrganizationSerializer


def test_org_serializer_validation_methods_exist():
    s = OrganizationSerializer()
    assert hasattr(s, 'validate_organization_id')
    assert hasattr(s, 'validate_organization_email')
