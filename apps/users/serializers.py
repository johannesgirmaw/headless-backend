"""
User serializers for the headless SaaS platform.
Handles serialization and validation of User data.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User
from apps.accounts.models import Account
from apps.organizations.models import Organization


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    # Computed fields
    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    effective_timezone = serializers.ReadOnlyField()
    effective_language = serializers.ReadOnlyField()

    # RBAC fields
    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'user_id',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'full_name',
            'display_name',
            'phone',
            'avatar',
            'account',
            'organization',
            'timezone',
            'language',
            'effective_timezone',
            'effective_language',
            'date_format',
            'time_format',
            'is_verified',
            'is_organization_admin',
            'is_account_admin',
            'preferences',
            'last_login_ip',
            'last_login_location',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'permissions',
            'roles',
            'groups',
        ]
        read_only_fields = [
            'id',
            'full_name',
            'display_name',
            'effective_timezone',
            'effective_language',
            'date_joined',
            'last_login',
            'last_login_ip',
            'last_login_location',
            'permissions',
            'roles',
            'groups',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_user_id(self, value):
        """Validate user_id uniqueness."""
        if self.instance and self.instance.user_id == value:
            return value

        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError(
                "A user with this ID already exists."
            )
        return value

    def validate_email(self, value):
        """Validate email uniqueness."""
        if self.instance and self.instance.email == value:
            return value

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_organization(self, value):
        """Validate organization belongs to the specified account."""
        account_id = self.initial_data.get('account')
        if account_id and value:
            # Convert both to strings for comparison
            if str(value.account_id) != str(account_id):
                raise serializers.ValidationError(
                    "Organization must belong to the specified account."
                )
        return value

    def create(self, validated_data):
        """Create a new user with hashed password."""
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """Update user instance."""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def get_permissions(self, obj):
        """Get all permissions for the user."""
        from apps.common.rbac_manager import get_rbac_manager

        organization_id = self.context.get('organization_id')
        rbac_manager = get_rbac_manager(obj)
        return list(rbac_manager.get_user_permissions(organization_id))

    def get_roles(self, obj):
        """Get all roles for the user."""
        from apps.common.rbac_manager import get_rbac_manager

        organization_id = self.context.get('organization_id')
        rbac_manager = get_rbac_manager(obj)
        return rbac_manager.get_user_roles(organization_id)

    def get_groups(self, obj):
        """Get all groups for the user."""
        from apps.common.rbac_manager import get_rbac_manager

        organization_id = self.context.get('organization_id')
        rbac_manager = get_rbac_manager(obj)
        return rbac_manager.get_user_groups(organization_id)


class UserCreateSerializer(UserSerializer):
    """Serializer for creating new users."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password']
        read_only_fields = UserSerializer.Meta.read_only_fields


class UserUpdateSerializer(UserSerializer):
    """Serializer for updating existing users."""

    password = serializers.CharField(
        write_only=True, min_length=8, required=False)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password']
        read_only_fields = UserSerializer.Meta.read_only_fields + [
            'user_id',  # User ID cannot be changed after creation
            'email',    # Email cannot be changed after creation
        ]


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for user lists."""

    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    account_name = serializers.CharField(
        source='account.company_name', read_only=True)
    organization_name = serializers.CharField(
        source='organization.organization_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'user_id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'display_name',
            'account_name',
            'organization_name',
            'is_verified',
            'is_organization_admin',
            'is_account_admin',
            'is_active',
            'last_login',
            'date_joined',
        ]


class UserDetailSerializer(UserSerializer):
    """Detailed serializer for user details."""

    # Add related data
    account_details = serializers.SerializerMethodField()
    organization_details = serializers.SerializerMethodField()
    team_memberships = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'account_details',
            'organization_details',
            'team_memberships',
        ]

    def get_account_details(self, obj):
        """Get account details."""
        if obj.account:
            return {
                'id': obj.account.id,
                'account_id': obj.account.account_id,
                'company_name': obj.account.company_name,
                'company_email': obj.account.company_email,
            }
        return None

    def get_organization_details(self, obj):
        """Get organization details."""
        if obj.organization:
            return {
                'id': obj.organization.id,
                'organization_id': obj.organization.organization_id,
                'organization_name': obj.organization.organization_name,
                'organization_email': obj.organization.organization_email,
            }
        return None

    def get_team_memberships(self, obj):
        """Get team memberships."""
        # TODO: Implement when we create team serializers
        return []


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Validate login credentials."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Invalid email or password.'
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )
            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                'Must include email and password.'
            )

        return attrs


class UserPasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing user password."""

    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def save(self):
        """Save new password."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
