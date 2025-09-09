from apps.organizations.serializers import OrganizationSerializer


def test_organization_serializer_has_computed_fields():
    s = OrganizationSerializer()
    assert 'full_address' in s.get_fields()
    assert 'effective_timezone' in s.get_fields()
    assert 'effective_language' in s.get_fields()
    assert 'effective_currency' in s.get_fields()
    assert 'user_count' in s.get_fields()
    assert 'team_count' in s.get_fields()
