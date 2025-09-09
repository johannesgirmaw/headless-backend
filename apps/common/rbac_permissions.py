from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from .rbac_manager import get_rbac_manager


class RBACPermission(permissions.BasePermission):
    """
    Custom permission class for Role-Based Access Control.

    This permission class checks if the user has the required permissions
    based on their roles, group memberships, and direct permissions.
    """

    def __init__(self, required_permissions=None, require_all=False):
        """
        Initialize RBAC permission.

        Args:
            required_permissions: List of permission codenames required
            require_all: If True, user must have all permissions. If False, user needs any permission.
        """
        self.required_permissions = required_permissions or []
        self.require_all = require_all

    def has_permission(self, request, view):
        """
        Check if user has required permissions.

        Args:
            request: HTTP request object
            view: View instance

        Returns:
            True if user has permission, False otherwise
        """
        if not request.user or not request.user.is_authenticated:
            return False

        if not self.required_permissions:
            return True

        rbac_manager = get_rbac_manager(request.user)

        # Get organization_id from request or view
        organization_id = getattr(request, 'organization_id', None)
        if not organization_id and hasattr(view, 'get_organization_id'):
            organization_id = view.get_organization_id(request)

        if self.require_all:
            return rbac_manager.has_all_permissions(self.required_permissions, organization_id)
        else:
            return rbac_manager.has_any_permission(self.required_permissions, organization_id)

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission for a specific object.

        Args:
            request: HTTP request object
            view: View instance
            obj: Object instance

        Returns:
            True if user has permission, False otherwise
        """
        return self.has_permission(request, view)


class ModelRBACPermission(RBACPermission):
    """
    Permission class that automatically determines required permissions based on model and action.
    """

    def __init__(self, model_name=None, actions=None):
        """
        Initialize model-based RBAC permission.

        Args:
            model_name: Name of the model (e.g., 'user', 'account')
            actions: Dictionary mapping actions to required permissions
        """
        self.model_name = model_name
        self.actions = actions or {}
        super().__init__()

    def get_required_permissions(self, request, view):
        """Get required permissions based on the action."""
        action = getattr(view, 'action', None)
        if not action:
            return []

        # Use provided actions or default mapping
        if self.actions and action in self.actions:
            return self.actions[action]

        # Default permission mapping
        if not self.model_name:
            # Try to get model name from view
            if hasattr(view, 'queryset') and view.queryset:
                self.model_name = view.queryset.model._meta.model_name

        if not self.model_name:
            return []

        default_actions = {
            'create': [f'{self.model_name}_create'],
            'read': [f'{self.model_name}_read'],
            'retrieve': [f'{self.model_name}_read'],
            'update': [f'{self.model_name}_update'],
            'partial_update': [f'{self.model_name}_update'],
            'destroy': [f'{self.model_name}_delete'],
            'delete': [f'{self.model_name}_delete'],
            'list': [f'{self.model_name}_list'],
        }

        return default_actions.get(action, [])

    def has_permission(self, request, view):
        """Check permission based on model and action."""
        if not request.user or not request.user.is_authenticated:
            return False

        required_permissions = self.get_required_permissions(request, view)
        if not required_permissions:
            return True

        rbac_manager = get_rbac_manager(request.user)

        # Get organization_id from request or view
        organization_id = getattr(request, 'organization_id', None)
        if not organization_id and hasattr(view, 'get_organization_id'):
            organization_id = view.get_organization_id(request)

        return rbac_manager.has_any_permission(required_permissions, organization_id)


class OrganizationPermission(permissions.BasePermission):
    """
    Permission class for organization-scoped resources.
    """

    def __init__(self, required_permissions=None):
        self.required_permissions = required_permissions or []

    def has_permission(self, request, view):
        """Check if user has permission within the organization."""
        if not request.user or not request.user.is_authenticated:
            return False

        # Get organization_id from URL or request
        organization_id = self.get_organization_id(request, view)
        if not organization_id:
            return False

        # Check if user belongs to the organization
        if not self.user_belongs_to_organization(request.user, organization_id):
            return False

        # Check specific permissions if required
        if self.required_permissions:
            rbac_manager = get_rbac_manager(request.user)
            return rbac_manager.has_any_permission(self.required_permissions, organization_id)

        return True

    def get_organization_id(self, request, view):
        """Extract organization_id from request or view."""
        # Try to get from URL parameters
        if hasattr(view, 'kwargs') and 'organization_id' in view.kwargs:
            return view.kwargs['organization_id']

        # Try to get from request data
        if hasattr(request, 'data') and 'organization_id' in request.data:
            return request.data['organization_id']

        # Try to get from query parameters
        organization_id = request.query_params.get('organization_id')
        if organization_id:
            return organization_id

        return None

    def user_belongs_to_organization(self, user, organization_id):
        """Check if user belongs to the organization."""
        return user.organization_id == organization_id


class AccountPermission(permissions.BasePermission):
    """
    Permission class for account-scoped resources.
    """

    def __init__(self, required_permissions=None):
        self.required_permissions = required_permissions or []

    def has_permission(self, request, view):
        """Check if user has permission within the account."""
        if not request.user or not request.user.is_authenticated:
            return False

        # Get account_id from URL or request
        account_id = self.get_account_id(request, view)
        if not account_id:
            return False

        # Check if user belongs to the account
        if not self.user_belongs_to_account(request.user, account_id):
            return False

        # Check specific permissions if required
        if self.required_permissions:
            rbac_manager = get_rbac_manager(request.user)
            return rbac_manager.has_any_permission(self.required_permissions, account_id)

        return True

    def get_account_id(self, request, view):
        """Extract account_id from request or view."""
        # Try to get from URL parameters
        if hasattr(view, 'kwargs') and 'account_id' in view.kwargs:
            return view.kwargs['account_id']

        # Try to get from request data
        if hasattr(request, 'data') and 'account_id' in request.data:
            return request.data['account_id']

        # Try to get from query parameters
        account_id = request.query_params.get('account_id')
        if account_id:
            return account_id

        return None

    def user_belongs_to_account(self, user, account_id):
        """Check if user belongs to the account."""
        return user.organization.account_id == account_id


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is the owner of the object."""
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.created_by == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners or admins to access objects.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is owner or admin."""
        # Allow if user is the owner
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True

        # Allow if user is admin
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Check RBAC permissions
        rbac_manager = get_rbac_manager(request.user)
        return rbac_manager.has_permission('admin_access')


class ReadOnlyPermission(permissions.BasePermission):
    """
    Permission class that only allows read operations.
    """

    def has_permission(self, request, view):
        """Only allow safe methods."""
        return request.method in permissions.SAFE_METHODS


class WriteOnlyPermission(permissions.BasePermission):
    """
    Permission class that only allows write operations.
    """

    def has_permission(self, request, view):
        """Only allow write methods."""
        return request.method not in permissions.SAFE_METHODS
