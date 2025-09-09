import pytest
from apps.organizations.models import Organization


def test_organization_limit_helpers_exist():
    assert hasattr(Organization, 'can_add_user')
    assert hasattr(Organization, 'can_add_team')
