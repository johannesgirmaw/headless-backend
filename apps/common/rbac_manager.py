from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from typing import List, Set, Dict, Any
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class RBACManager:
    """Manager class for handling Role-Based Access Control operations."""

    def __init__(self, user: User):
        self.user = user

    def get_user_permissions(self, organization_id: str = None) -> Set[str]:
        """
        Get all permissions for a user from roles, groups, and direct assignments.

        Args:
            organization_id: Optional organization ID to filter permissions

        Returns:
            Set of permission codenames
        """
        permissions = set()

        # Get permissions from user roles
        user_roles = self.user.rbac_user_roles.filter(
            is_active=True,
            expires_at__isnull=True
        ) | self.user.rbac_user_roles.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )

        if organization_id:
            user_roles = user_roles.filter(
                role__organization_id=organization_id)

        for user_role in user_roles:
            role_permissions = user_role.role.role_permissions.filter(
                permission__is_active=True
            )
            permissions.update(
                [rp.permission.codename for rp in role_permissions])

        # Get permissions from group memberships
        group_memberships = self.user.rbac_group_memberships.filter(
            is_active=True,
            expires_at__isnull=True
        ) | self.user.rbac_group_memberships.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )

        if organization_id:
            group_memberships = group_memberships.filter(
                group__organization_id=organization_id)

        for membership in group_memberships:
            # Get permissions from group roles
            group_roles = membership.group.group_roles.filter(
                is_active=True,
                expires_at__isnull=True
            ) | membership.group.group_roles.filter(
                is_active=True,
                expires_at__gt=timezone.now()
            )

            for group_role in group_roles:
                role_permissions = group_role.role.role_permissions.filter(
                    permission__is_active=True
                )
                permissions.update(
                    [rp.permission.codename for rp in role_permissions])

            # Get direct group permissions
            group_permissions = membership.group.group_permissions.filter(
                is_active=True,
                expires_at__isnull=True
            ) | membership.group.group_permissions.filter(
                is_active=True,
                expires_at__gt=timezone.now()
            )

            permissions.update(
                [gp.permission.codename for gp in group_permissions])

        # Get direct user permissions
        user_permissions = self.user.rbac_user_permissions.filter(
            is_active=True,
            expires_at__isnull=True
        ) | self.user.rbac_user_permissions.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )

        permissions.update([up.permission.codename for up in user_permissions])

        return permissions

    def has_permission(self, permission_codename: str, organization_id: str = None) -> bool:
        """
        Check if user has a specific permission.

        Args:
            permission_codename: Permission codename to check
            organization_id: Optional organization ID to filter permissions

        Returns:
            True if user has permission, False otherwise
        """
        permissions = self.get_user_permissions(organization_id)
        return permission_codename in permissions

    def has_any_permission(self, permission_codenames: List[str], organization_id: str = None) -> bool:
        """
        Check if user has any of the specified permissions.

        Args:
            permission_codenames: List of permission codenames to check
            organization_id: Optional organization ID to filter permissions

        Returns:
            True if user has any of the permissions, False otherwise
        """
        permissions = self.get_user_permissions(organization_id)
        return any(perm in permissions for perm in permission_codenames)

    def has_all_permissions(self, permission_codenames: List[str], organization_id: str = None) -> bool:
        """
        Check if user has all of the specified permissions.

        Args:
            permission_codenames: List of permission codenames to check
            organization_id: Optional organization ID to filter permissions

        Returns:
            True if user has all permissions, False otherwise
        """
        permissions = self.get_user_permissions(organization_id)
        return all(perm in permissions for perm in permission_codenames)

    def get_user_roles(self, organization_id: str = None) -> List[Dict[str, Any]]:
        """
        Get all roles assigned to the user.

        Args:
            organization_id: Optional organization ID to filter roles

        Returns:
            List of role information dictionaries
        """
        rbac_user_roles = self.user.rbac_user_roles.filter(
            is_active=True,
            expires_at__isnull=True
        ) | self.user.rbac_user_roles.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )

        if organization_id:
            rbac_user_roles = rbac_user_roles.filter(
                role__organization_id=organization_id)

        roles = []
        for user_role in rbac_user_roles:
            roles.append({
                'id': str(user_role.role.id),
                'name': user_role.role.name,
                'codename': user_role.role.codename,
                'description': user_role.role.description,
                'role_type': user_role.role.role_type,
                'organization_id': str(user_role.role.organization_id) if user_role.role.organization else None,
                'assigned_at': user_role.assigned_at,
                'expires_at': user_role.expires_at,
            })

        return roles

    def get_user_groups(self, organization_id: str = None) -> List[Dict[str, Any]]:
        """
        Get all groups the user belongs to.

        Args:
            organization_id: Optional organization ID to filter groups

        Returns:
            List of group information dictionaries
        """
        group_memberships = self.user.rbac_group_memberships.filter(
            is_active=True,
            expires_at__isnull=True
        ) | self.user.rbac_group_memberships.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )

        if organization_id:
            group_memberships = group_memberships.filter(
                group__organization_id=organization_id)

        groups = []
        for membership in group_memberships:
            groups.append({
                'id': str(membership.group.id),
                'name': membership.group.name,
                'description': membership.group.description,
                'organization_id': str(membership.group.organization_id),
                'added_at': membership.added_at,
                'expires_at': membership.expires_at,
            })

        return groups

    def get_permission_details(self, organization_id: str = None) -> Dict[str, Any]:
        """
        Get detailed permission information for the user.

        Args:
            organization_id: Optional organization ID to filter permissions

        Returns:
            Dictionary with permission details
        """
        permissions = self.get_user_permissions(organization_id)
        roles = self.get_user_roles(organization_id)
        groups = self.get_user_groups(organization_id)

        return {
            'user_id': str(self.user.id),
            'email': self.user.email,
            'permissions': list(permissions),
            'roles': roles,
            'groups': groups,
            'organization_id': organization_id,
        }


def get_rbac_manager(user: User) -> RBACManager:
    """Get RBAC manager instance for a user."""
    return RBACManager(user)


def check_permission(user: User, permission_codename: str, organization_id: str = None) -> bool:
    """Quick permission check function."""
    rbac_manager = get_rbac_manager(user)
    return rbac_manager.has_permission(permission_codename, organization_id)


def require_permission(permission_codename: str, organization_id: str = None):
    """Decorator to require a specific permission."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not check_permission(request.user, permission_codename, organization_id):
                raise PermissionDenied(
                    f"Permission required: {permission_codename}")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


class RBACPermissionMixin:
    """Mixin for viewsets to add RBAC permission checking."""

    def get_required_permissions(self, action: str) -> List[str]:
        """
        Get required permissions for a specific action.
        Override this method in your viewset to define required permissions.

        Args:
            action: Action name (create, read, update, delete, list)

        Returns:
            List of required permission codenames
        """
        model_name = self.queryset.model._meta.model_name
        permissions_map = {
            'create': [f'{model_name}_create'],
            'read': [f'{model_name}_read'],
            'update': [f'{model_name}_update'],
            'delete': [f'{model_name}_delete'],
            'list': [f'{model_name}_list'],
        }
        return permissions_map.get(action, [])

    def check_permissions(self, request, action: str = None):
        """Check if user has required permissions for the action."""
        if not action:
            action = self.action

        required_permissions = self.get_required_permissions(action)
        if not required_permissions:
            return True

        rbac_manager = get_rbac_manager(request.user)

        # Get organization_id from request or context
        organization_id = getattr(request, 'organization_id', None)
        if not organization_id and hasattr(self, 'get_organization_id'):
            organization_id = self.get_organization_id(request)

        if not rbac_manager.has_any_permission(required_permissions, organization_id):
            raise PermissionDenied(
                f"Required permissions: {', '.join(required_permissions)}")

        return True
