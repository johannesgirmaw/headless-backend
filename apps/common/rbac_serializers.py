from rest_framework import serializers
from django.contrib.auth import get_user_model
from .rbac_models import (
    Permission, Role, UserGroup, RolePermission, UserRole,
    UserPermission, GroupPermission, UserGroupMembership, RoleGroup
)

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model."""

    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'codename', 'description', 'permission_type',
            'model_name', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PermissionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for permission lists."""

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename',
                  'permission_type', 'model_name', 'is_active']


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""

    organization_name = serializers.CharField(
        source='organization.name', read_only=True)
    permission_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'codename', 'description', 'role_type',
            'organization', 'organization_name', 'is_active', 'is_system_role',
            'permission_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_permission_count(self, obj):
        """Get the number of permissions assigned to this role."""
        return obj.role_permissions.filter(permission__is_active=True).count()


class RoleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for role lists."""

    organization_name = serializers.CharField(
        source='organization.name', read_only=True)
    permission_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'codename', 'role_type', 'organization_name',
            'is_active', 'permission_count'
        ]

    def get_permission_count(self, obj):
        """Get the number of permissions assigned to this role."""
        return obj.role_permissions.filter(permission__is_active=True).count()


class RolePermissionSerializer(serializers.ModelSerializer):
    """Serializer for RolePermission model."""

    permission_name = serializers.CharField(
        source='permission.name', read_only=True)
    permission_codename = serializers.CharField(
        source='permission.codename', read_only=True)
    granted_by_name = serializers.CharField(
        source='granted_by.email', read_only=True)

    class Meta:
        model = RolePermission
        fields = [
            'id', 'role', 'permission', 'permission_name', 'permission_codename',
            'granted_by', 'granted_by_name', 'granted_at'
        ]
        read_only_fields = ['id', 'granted_at']


class UserGroupSerializer(serializers.ModelSerializer):
    """Serializer for UserGroup model."""

    organization_name = serializers.CharField(
        source='organization.name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.email', read_only=True)
    member_count = serializers.SerializerMethodField()
    role_count = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = [
            'id', 'name', 'description', 'organization', 'organization_name',
            'is_active', 'created_by', 'created_by_name', 'member_count',
            'role_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        """Get the number of members in this group."""
        return obj.group_memberships.filter(is_active=True).count()

    def get_role_count(self, obj):
        """Get the number of roles assigned to this group."""
        return obj.group_roles.filter(is_active=True).count()


class UserGroupListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for user group lists."""

    organization_name = serializers.CharField(
        source='organization.name', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = [
            'id', 'name', 'organization_name', 'is_active', 'member_count'
        ]

    def get_member_count(self, obj):
        """Get the number of members in this group."""
        return obj.group_memberships.filter(is_active=True).count()


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole model."""

    role_name = serializers.CharField(source='role.name', read_only=True)
    role_codename = serializers.CharField(
        source='role.codename', read_only=True)
    assigned_by_name = serializers.CharField(
        source='assigned_by.email', read_only=True)

    class Meta:
        model = UserRole
        fields = [
            'id', 'user', 'role', 'role_name', 'role_codename',
            'assigned_by', 'assigned_by_name', 'assigned_at',
            'expires_at', 'is_active'
        ]
        read_only_fields = ['id', 'assigned_at']


class UserPermissionSerializer(serializers.ModelSerializer):
    """Serializer for UserPermission model."""

    permission_name = serializers.CharField(
        source='permission.name', read_only=True)
    permission_codename = serializers.CharField(
        source='permission.codename', read_only=True)
    granted_by_name = serializers.CharField(
        source='granted_by.email', read_only=True)

    class Meta:
        model = UserPermission
        fields = [
            'id', 'user', 'permission', 'permission_name', 'permission_codename',
            'granted_by', 'granted_by_name', 'granted_at', 'expires_at', 'is_active'
        ]
        read_only_fields = ['id', 'granted_at']


class GroupPermissionSerializer(serializers.ModelSerializer):
    """Serializer for GroupPermission model."""

    permission_name = serializers.CharField(
        source='permission.name', read_only=True)
    permission_codename = serializers.CharField(
        source='permission.codename', read_only=True)
    granted_by_name = serializers.CharField(
        source='granted_by.email', read_only=True)

    class Meta:
        model = GroupPermission
        fields = [
            'id', 'group', 'permission', 'permission_name', 'permission_codename',
            'granted_by', 'granted_by_name', 'granted_at', 'expires_at', 'is_active'
        ]
        read_only_fields = ['id', 'granted_at']


class UserGroupMembershipSerializer(serializers.ModelSerializer):
    """Serializer for UserGroupMembership model."""

    user_name = serializers.CharField(source='user.email', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    added_by_name = serializers.CharField(
        source='added_by.email', read_only=True)

    class Meta:
        model = UserGroupMembership
        fields = [
            'id', 'user', 'group', 'user_name', 'group_name',
            'added_by', 'added_by_name', 'added_at', 'expires_at', 'is_active'
        ]
        read_only_fields = ['id', 'added_at']


class RoleGroupSerializer(serializers.ModelSerializer):
    """Serializer for RoleGroup model."""

    role_name = serializers.CharField(source='role.name', read_only=True)
    role_codename = serializers.CharField(
        source='role.codename', read_only=True)
    assigned_by_name = serializers.CharField(
        source='assigned_by.email', read_only=True)

    class Meta:
        model = RoleGroup
        fields = [
            'id', 'group', 'role', 'role_name', 'role_codename',
            'assigned_by', 'assigned_by_name', 'assigned_at', 'expires_at', 'is_active'
        ]
        read_only_fields = ['id', 'assigned_at']


class UserRBACSerializer(serializers.ModelSerializer):
    """Serializer for user RBAC information."""

    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'permissions', 'roles', 'groups'
        ]

    def get_permissions(self, obj):
        """Get all permissions for the user."""
        from .rbac_manager import get_rbac_manager

        organization_id = self.context.get('organization_id')
        rbac_manager = get_rbac_manager(obj)
        return rbac_manager.get_user_permissions(organization_id)

    def get_roles(self, obj):
        """Get all roles for the user."""
        from .rbac_manager import get_rbac_manager

        organization_id = self.context.get('organization_id')
        rbac_manager = get_rbac_manager(obj)
        return rbac_manager.get_user_roles(organization_id)

    def get_groups(self, obj):
        """Get all groups for the user."""
        from .rbac_manager import get_rbac_manager

        organization_id = self.context.get('organization_id')
        rbac_manager = get_rbac_manager(obj)
        return rbac_manager.get_user_groups(organization_id)


class AssignRoleSerializer(serializers.Serializer):
    """Serializer for assigning roles to users."""

    role_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="List of role IDs to assign"
    )
    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Optional expiration date for the role assignment"
    )

    def validate_role_ids(self, value):
        """Validate that all role IDs exist."""
        from .rbac_models import Role

        existing_roles = Role.objects.filter(id__in=value, is_active=True)
        if len(existing_roles) != len(value):
            raise serializers.ValidationError(
                "One or more role IDs are invalid or inactive.")

        return value


class AssignPermissionSerializer(serializers.Serializer):
    """Serializer for assigning permissions to users or groups."""

    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="List of permission IDs to assign"
    )
    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Optional expiration date for the permission assignment"
    )

    def validate_permission_ids(self, value):
        """Validate that all permission IDs exist."""
        from .rbac_models import Permission

        existing_permissions = Permission.objects.filter(
            id__in=value, is_active=True)
        if len(existing_permissions) != len(value):
            raise serializers.ValidationError(
                "One or more permission IDs are invalid or inactive.")

        return value


class AddToGroupSerializer(serializers.Serializer):
    """Serializer for adding users to groups."""

    user_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="List of user IDs to add to the group"
    )
    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Optional expiration date for the group membership"
    )

    def validate_user_ids(self, value):
        """Validate that all user IDs exist."""
        existing_users = User.objects.filter(id__in=value, is_active=True)
        if len(existing_users) != len(value):
            raise serializers.ValidationError(
                "One or more user IDs are invalid or inactive.")

        return value
