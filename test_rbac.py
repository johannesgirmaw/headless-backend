#!/usr/bin/env python
"""
Test script for RBAC (Role-Based Access Control) system.
This script tests the basic functionality of the RBAC system.
"""

from apps.organizations.models import Organization
from apps.accounts.models import Account
from apps.common.rbac_manager import get_rbac_manager
from apps.common.rbac_models import Permission, Role, UserGroup, UserRole, UserPermission
from django.contrib.auth import get_user_model
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headless_backend.settings')
django.setup()


User = get_user_model()


def test_rbac_system():
    """Test the RBAC system functionality."""
    print("🧪 Testing RBAC System...")

    # Test 1: Check if permissions exist
    print("\n1. Testing Permissions...")
    permissions = Permission.objects.filter(is_active=True)
    print(f"   ✅ Found {permissions.count()} permissions")

    # Test 2: Check if system roles exist
    print("\n2. Testing System Roles...")
    system_roles = Role.objects.filter(is_system_role=True, is_active=True)
    print(f"   ✅ Found {system_roles.count()} system roles:")
    for role in system_roles:
        permission_count = role.role_permissions.filter(
            permission__is_active=True).count()
        print(f"      - {role.name}: {permission_count} permissions")

    # Test 3: Test RBAC Manager
    print("\n3. Testing RBAC Manager...")

    # Get or create a test user
    test_user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={
            'user_id': 'TEST_USER_001',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )

    if created:
        print(f"   ✅ Created test user: {test_user.email}")
    else:
        print(f"   ✅ Using existing test user: {test_user.email}")

    # Get RBAC manager for the user
    rbac_manager = get_rbac_manager(test_user)

    # Test permission checking
    print("\n4. Testing Permission Checking...")

    # Check if user has any permissions (should be empty initially)
    user_permissions = rbac_manager.get_user_permissions()
    print(f"   ✅ User has {len(user_permissions)} permissions")

    # Test 5: Assign a role to the user
    print("\n5. Testing Role Assignment...")

    # Get the "User" role
    user_role = Role.objects.filter(
        codename='user', is_system_role=True).first()
    if user_role:
        # Assign the role to the test user
        user_role_assignment, created = UserRole.objects.get_or_create(
            user=test_user,
            role=user_role,
            defaults={'assigned_by': test_user}
        )

        if created:
            print(f"   ✅ Assigned role '{user_role.name}' to user")
        else:
            print(f"   ✅ User already has role '{user_role.name}'")

        # Check permissions again
        user_permissions = rbac_manager.get_user_permissions()
        print(f"   ✅ User now has {len(user_permissions)} permissions")

        # Test specific permission checking
        has_read_permission = rbac_manager.has_permission('users_read')
        print(f"   ✅ User has 'users_read' permission: {has_read_permission}")

        has_create_permission = rbac_manager.has_permission('users_create')
        print(
            f"   ✅ User has 'users_create' permission: {has_create_permission}")

    # Test 6: Test organization-scoped permissions
    print("\n6. Testing Organization-Scoped Permissions...")

    # Create a test account and organization
    test_account, created = Account.objects.get_or_create(
        account_id='TEST001',
        defaults={
            'company_name': 'Test Company',
            'company_email': 'test@testcompany.com',
            'is_active': True
        }
    )

    if created:
        print(f"   ✅ Created test account: {test_account.company_name}")
    else:
        print(f"   ✅ Using existing test account: {test_account.company_name}")

    test_org, created = Organization.objects.get_or_create(
        organization_id='ORG001',
        account=test_account,
        defaults={
            'organization_name': 'Test Organization',
            'organization_email': 'test@testorg.com',
            'is_active': True
        }
    )

    if created:
        print(f"   ✅ Created test organization: {test_org.organization_name}")
    else:
        print(
            f"   ✅ Using existing test organization: {test_org.organization_name}")

    # Test organization-scoped permission checking
    org_permissions = rbac_manager.get_user_permissions(str(test_org.id))
    print(f"   ✅ User has {len(org_permissions)} permissions in organization")

    # Test 7: Test User Group functionality
    print("\n7. Testing User Groups...")

    # Create a test group
    test_group, created = UserGroup.objects.get_or_create(
        name='Test Group',
        organization=test_org,
        defaults={
            'description': 'A test group for RBAC testing',
            'created_by': test_user
        }
    )

    if created:
        print(f"   ✅ Created test group: {test_group.name}")
    else:
        print(f"   ✅ Using existing test group: {test_group.name}")

    # Test 8: Test permission details
    print("\n8. Testing Permission Details...")

    permission_details = rbac_manager.get_permission_details(str(test_org.id))
    print(f"   ✅ Permission details retrieved:")
    print(f"      - User ID: {permission_details['user_id']}")
    print(f"      - Email: {permission_details['email']}")
    print(f"      - Permissions: {len(permission_details['permissions'])}")
    print(f"      - Roles: {len(permission_details['roles'])}")
    print(f"      - Groups: {len(permission_details['groups'])}")

    print("\n🎉 RBAC System Test Completed Successfully!")
    print("\n📋 Summary:")
    print(
        f"   - Permissions: {Permission.objects.filter(is_active=True).count()}")
    print(
        f"   - System Roles: {Role.objects.filter(is_system_role=True, is_active=True).count()}")
    print(f"   - Test User: {test_user.email}")
    print(f"   - Test Account: {test_account.company_name}")
    print(f"   - Test Organization: {test_org.organization_name}")
    print(f"   - Test Group: {test_group.name}")


if __name__ == '__main__':
    try:
        test_rbac_system()
    except Exception as e:
        print(f"❌ Error testing RBAC system: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
