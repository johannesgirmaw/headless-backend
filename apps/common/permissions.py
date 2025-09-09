"""
Custom permissions for the headless SaaS platform.
Handles multi-tenant access control and role-based permissions.
"""

from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class IsAccountAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to account administrators.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        return request.user.is_account_admin


class IsOrganizationAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to organization administrators.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        return request.user.is_organization_admin or request.user.is_account_admin


class IsAccountMember(permissions.BasePermission):
    """
    Permission class that allows access only to account members.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        return request.user.account is not None


class IsOrganizationMember(permissions.BasePermission):
    """
    Permission class that allows access only to organization members.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        return request.user.organization is not None


class IsTeamOwner(permissions.BasePermission):
    """
    Permission class that allows access only to team owners.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        # Check if user is a team owner in any team
        from apps.teams.models import TeamMember
        return TeamMember.objects.filter(
            user=request.user,
            role='owner'
        ).exists()


class IsTeamAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to team administrators.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        # Check if user is a team admin or owner in any team
        from apps.teams.models import TeamMember
        return TeamMember.objects.filter(
            user=request.user,
            role__in=['owner', 'admin']
        ).exists()


class IsTeamMember(permissions.BasePermission):
    """
    Permission class that allows access only to team members.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        # Check if user is a member of any team
        from apps.teams.models import TeamMember
        return TeamMember.objects.filter(
            user=request.user,
            status='active'
        ).exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.created_by == request.user


class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow account owners to edit account-related objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to account administrators.
        return request.user.is_account_admin


class IsOrganizationOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organization owners to edit organization-related objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to organization administrators.
        return request.user.is_organization_admin or request.user.is_account_admin


class IsTeamOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow team owners to edit team-related objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to team owners.
        from apps.teams.models import TeamMember
        try:
            membership = TeamMember.objects.get(team=obj, user=request.user)
            return membership.role == 'owner'
        except TeamMember.DoesNotExist:
            return False


class IsTeamAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow team administrators to edit team-related objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to team administrators.
        from apps.teams.models import TeamMember
        try:
            membership = TeamMember.objects.get(team=obj, user=request.user)
            return membership.role in ['owner', 'admin']
        except TeamMember.DoesNotExist:
            return False


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile or admins to edit any profile.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the user themselves or administrators.
        return obj == request.user or request.user.is_staff or request.user.is_account_admin


class MultiTenantPermission(permissions.BasePermission):
    """
    Custom permission that ensures users can only access data within their account/organization.
    """

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False

        # Allow access if user has an account
        return request.user.account is not None

    def has_object_permission(self, request, view, obj):
        # Check if the object belongs to the user's account
        if hasattr(obj, 'account'):
            return obj.account == request.user.account

        # Check if the object belongs to the user's organization
        if hasattr(obj, 'organization'):
            return obj.organization == request.user.organization

        # Check if the object belongs to the user's account through organization
        if hasattr(obj, 'account') and hasattr(obj, 'organization'):
            return (obj.account == request.user.account and
                    obj.organization == request.user.organization)

        # If object doesn't have account/organization fields, allow access
        return True
