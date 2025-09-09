from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


class Permission(models.Model):
    """System-wide permissions for different actions on different models."""

    PERMISSION_TYPES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('list', 'List'),
        ('manage', 'Manage'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True,
                            help_text="Permission name (e.g., 'users:create')")
    codename = models.CharField(
        max_length=100, unique=True, help_text="Permission codename (e.g., 'users_create')")
    description = models.TextField(
        blank=True, help_text="Permission description")
    permission_type = models.CharField(
        max_length=20, choices=PERMISSION_TYPES, help_text="Type of permission")
    model_name = models.CharField(
        max_length=50, help_text="Model name (e.g., 'user', 'account')")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rbac_permissions'
        ordering = ['model_name', 'permission_type']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return f"{self.name} ({self.codename})"

    def clean(self):
        if not self.codename:
            self.codename = f"{self.model_name}_{self.permission_type}"
        if not self.name:
            self.name = f"{self.model_name}:{self.permission_type}"


class Role(models.Model):
    """Roles that can be assigned to users or groups."""

    ROLE_TYPES = [
        ('system', 'System Role'),
        ('organization', 'Organization Role'),
        ('custom', 'Custom Role'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Role name")
    codename = models.CharField(max_length=100, help_text="Role codename")
    description = models.TextField(blank=True, help_text="Role description")
    role_type = models.CharField(
        max_length=20, choices=ROLE_TYPES, default='custom')
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Organization this role belongs to (null for system roles)"
    )
    is_active = models.BooleanField(default=True)
    is_system_role = models.BooleanField(
        default=False, help_text="System-defined role that cannot be deleted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rbac_roles'
        ordering = ['role_type', 'name']
        unique_together = ['codename', 'organization']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        org_suffix = f" ({self.organization.name})" if self.organization else " (System)"
        return f"{self.name}{org_suffix}"

    def clean(self):
        if self.role_type == 'system' and self.organization:
            raise ValidationError(
                "System roles cannot belong to an organization")
        if self.role_type in ['organization', 'custom'] and not self.organization:
            raise ValidationError(
                "Organization and custom roles must belong to an organization")


class UserGroup(models.Model):
    """Groups of users within an organization."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Group name")
    description = models.TextField(blank=True, help_text="Group description")
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        help_text="Organization this group belongs to"
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_groups',
        help_text="User who created this group"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rbac_user_groups'
        ordering = ['name']
        unique_together = ['name', 'organization']
        verbose_name = 'User Group'
        verbose_name_plural = 'User Groups'

    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class RolePermission(models.Model):
    """Many-to-many relationship between roles and permissions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name='role_permissions')
    granted_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text="User who granted this permission"
    )
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rbac_role_permissions'
        unique_together = ['role', 'permission']
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'

    def __str__(self):
        return f"{self.role.name} -> {self.permission.name}"


class UserRole(models.Model):
    """Many-to-many relationship between users and roles."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='rbac_user_roles')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_roles',
        help_text="User who assigned this role"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="Role expiration date")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'rbac_user_roles'
        unique_together = ['user', 'role']
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'

    def __str__(self):
        return f"{self.user.email} -> {self.role.name}"

    def clean(self):
        if self.expires_at and self.expires_at <= self.assigned_at:
            raise ValidationError(
                "Expiration date must be after assignment date")


class UserPermission(models.Model):
    """Direct permissions assigned to individual users."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='rbac_user_permissions')
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name='user_permissions')
    granted_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='granted_permissions',
        help_text="User who granted this permission"
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="Permission expiration date")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'rbac_user_permissions'
        unique_together = ['user', 'permission']
        verbose_name = 'User Permission'
        verbose_name_plural = 'User Permissions'

    def __str__(self):
        return f"{self.user.email} -> {self.permission.name}"

    def clean(self):
        if self.expires_at and self.expires_at <= self.granted_at:
            raise ValidationError("Expiration date must be after grant date")


class GroupPermission(models.Model):
    """Permissions assigned to user groups."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name='group_permissions')
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name='group_permissions')
    granted_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text="User who granted this permission"
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="Permission expiration date")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'rbac_group_permissions'
        unique_together = ['group', 'permission']
        verbose_name = 'Group Permission'
        verbose_name_plural = 'Group Permissions'

    def __str__(self):
        return f"{self.group.name} -> {self.permission.name}"


class UserGroupMembership(models.Model):
    """Many-to-many relationship between users and groups."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='rbac_group_memberships')
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name='group_memberships')
    added_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='added_to_groups',
        help_text="User who added this user to the group"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="Membership expiration date")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'rbac_user_group_memberships'
        unique_together = ['user', 'group']
        verbose_name = 'User Group Membership'
        verbose_name_plural = 'User Group Memberships'

    def __str__(self):
        return f"{self.user.email} -> {self.group.name}"

    def clean(self):
        if self.expires_at and self.expires_at <= self.added_at:
            raise ValidationError(
                "Expiration date must be after addition date")


class RoleGroup(models.Model):
    """Roles assigned to user groups."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name='group_roles')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='group_roles')
    assigned_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_group_roles',
        help_text="User who assigned this role to the group"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="Role expiration date")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'rbac_group_roles'
        unique_together = ['group', 'role']
        verbose_name = 'Group Role'
        verbose_name_plural = 'Group Roles'

    def __str__(self):
        return f"{self.group.name} -> {self.role.name}"
