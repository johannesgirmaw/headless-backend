"""
Account serializers for the headless SaaS platform.
Handles serialization and validation of Account data.
"""

from rest_framework import serializers
from apps.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model."""

    # Computed fields
    full_address = serializers.ReadOnlyField()
    is_subscription_active = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = [
            'id',
            'account_id',
            'name',
            'description',
            'is_active',
            'company_name',
            'company_email',
            'company_phone',
            'company_website',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'full_address',
            'timezone',
            'language',
            'currency',
            'subscription_plan',
            'subscription_status',
            'subscription_start_date',
            'subscription_end_date',
            'is_subscription_active',
            'max_organizations',
            'max_users_per_organization',
            'max_storage_gb',
            'features',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'full_address',
            'is_subscription_active',
        ]

    def validate_account_id(self, value):
        """Validate account_id uniqueness."""
        if self.instance and self.instance.account_id == value:
            return value

        if Account.objects.filter(account_id=value).exists():
            raise serializers.ValidationError(
                "An account with this ID already exists."
            )
        return value

    def validate_company_email(self, value):
        """Validate company email uniqueness."""
        if self.instance and self.instance.company_email == value:
            return value

        if Account.objects.filter(company_email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def validate_subscription_end_date(self, value):
        """Validate subscription end date."""
        subscription_start_date = self.initial_data.get(
            'subscription_start_date')
        if subscription_start_date and value and value <= subscription_start_date:
            raise serializers.ValidationError(
                "Subscription end date must be after start date."
            )
        return value


class AccountCreateSerializer(AccountSerializer):
    """Serializer for creating new accounts."""

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'full_address',
            'is_subscription_active',
        ]


class AccountUpdateSerializer(AccountSerializer):
    """Serializer for updating existing accounts."""

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields
        read_only_fields = [
            'id',
            'account_id',  # Account ID cannot be changed after creation
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'full_address',
            'is_subscription_active',
        ]


class AccountListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for account lists."""

    full_address = serializers.SerializerMethodField()
    is_subscription_active = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id',
            'account_id',
            'name',
            'company_name',
            'company_email',
            'subscription_status',
            'is_subscription_active',
            'full_address',
            'max_organizations',
            'max_users_per_organization',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_full_address(self, obj):
        """Get the full address."""
        return obj.full_address

    def get_is_subscription_active(self, obj):
        """Get subscription active status."""
        return obj.is_subscription_active


class AccountDetailSerializer(AccountSerializer):
    """Detailed serializer for account details."""

    # Add related data
    organizations_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + [
            'organizations_count',
            'users_count',
        ]

    def get_organizations_count(self, obj):
        """Get the number of organizations in this account."""
        return obj.organizations.filter(deleted_at__isnull=True).count()

    def get_users_count(self, obj):
        """Get the number of users in this account."""
        return obj.users.filter(deleted_at__isnull=True).count()
