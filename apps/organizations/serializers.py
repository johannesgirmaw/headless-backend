"""
Organization serializers for the headless SaaS platform.
Handles serialization and validation of Organization data.
"""

from rest_framework import serializers
from apps.organizations.models import Organization, Subscription
from apps.accounts.models import Account


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model."""

    # Computed fields
    full_address = serializers.ReadOnlyField()
    effective_timezone = serializers.ReadOnlyField()
    effective_language = serializers.ReadOnlyField()
    effective_currency = serializers.ReadOnlyField()
    user_count = serializers.SerializerMethodField()
    team_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id',
            'organization_id',
            'name',
            'description',
            'is_active',
            'account',
            'organization_name',
            'organization_email',
            'organization_phone',
            'organization_website',
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
            'effective_timezone',
            'effective_language',
            'effective_currency',
            'max_users',
            'max_teams',
            'max_storage_gb',
            'features',
            'status',
            'user_count',
            'team_count',
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
            'effective_timezone',
            'effective_language',
            'effective_currency',
            'user_count',
            'team_count',
        ]

    def validate_organization_id(self, value):
        """Validate organization_id uniqueness within account."""
        account_id = self.initial_data.get('account')
        if not account_id:
            raise serializers.ValidationError("Account is required.")

        if self.instance and self.instance.organization_id == value:
            return value

        if Organization.objects.filter(
            account_id=account_id,
            organization_id=value
        ).exists():
            raise serializers.ValidationError(
                "An organization with this ID already exists in this account."
            )
        return value

    def validate_organization_email(self, value):
        """Validate organization email uniqueness within account."""
        account_id = self.initial_data.get('account')
        if not value or not account_id:
            return value

        if self.instance and self.instance.organization_email == value:
            return value

        if Organization.objects.filter(
            account_id=account_id,
            organization_email=value
        ).exists():
            raise serializers.ValidationError(
                "An organization with this email already exists in this account."
            )
        return value

    def validate_max_users(self, value):
        """Validate max_users against account limits."""
        account_id = self.initial_data.get('account')
        if account_id:
            try:
                account = Account.objects.get(id=account_id)
                if value > account.max_users_per_organization:
                    raise serializers.ValidationError(
                        f"Max users cannot exceed account limit of {account.max_users_per_organization}."
                    )
            except Account.DoesNotExist:
                raise serializers.ValidationError("Invalid account ID.")
        return value

    def get_user_count(self, obj):
        """Get the current number of users in this organization."""
        return obj.get_user_count()

    def get_team_count(self, obj):
        """Get the current number of teams in this organization."""
        return obj.get_team_count()


class OrganizationCreateSerializer(OrganizationSerializer):
    """Serializer for creating new organizations."""

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields
        read_only_fields = OrganizationSerializer.Meta.read_only_fields


class OrganizationUpdateSerializer(OrganizationSerializer):
    """Serializer for updating existing organizations."""

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields
        read_only_fields = OrganizationSerializer.Meta.read_only_fields + [
            'organization_id',  # Organization ID cannot be changed after creation
            'account',  # Account cannot be changed after creation
        ]


class OrganizationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for organization lists."""

    full_address = serializers.SerializerMethodField()
    effective_timezone = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()
    team_count = serializers.SerializerMethodField()
    account_name = serializers.CharField(
        source='account.company_name', read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id',
            'organization_id',
            'name',
            'organization_name',
            'organization_email',
            'account_name',
            'status',
            'max_users',
            'max_teams',
            'user_count',
            'team_count',
            'full_address',
            'effective_timezone',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_full_address(self, obj):
        """Get the full address."""
        return obj.full_address

    def get_effective_timezone(self, obj):
        """Get the effective timezone."""
        return obj.effective_timezone

    def get_user_count(self, obj):
        """Get the current number of users in this organization."""
        return obj.get_user_count()

    def get_team_count(self, obj):
        """Get the current number of teams in this organization."""
        return obj.get_team_count()


class OrganizationDetailSerializer(OrganizationSerializer):
    """Detailed serializer for organization details."""

    # Add related data
    account_details = serializers.SerializerMethodField()

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + [
            'account_details',
        ]

    def get_account_details(self, obj):
        """Get account details."""
        return {
            'id': obj.account.id,
            'account_id': obj.account.account_id,
            'company_name': obj.account.company_name,
            'company_email': obj.account.company_email,
            'subscription_status': obj.account.subscription_status,
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model with API field mapping."""

    subscriptionId = serializers.IntegerField(source='id', read_only=True)
    organizationId = serializers.SerializerMethodField(read_only=True)
    productId = serializers.IntegerField(source='product_id')
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    status = serializers.CharField()
    planConfiguration = serializers.JSONField(source='plan_configuration')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'subscriptionId', 'organizationId', 'productId', 'startDate', 'endDate',
            'status', 'planConfiguration', 'createdAt', 'updatedAt'
        ]

    def get_organizationId(self, obj):
        return obj.organization_id

    def validate(self, attrs):
        # date order validation
        start = attrs.get('start_date')
        end = attrs.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError(
                'endDate must be after startDate')
        return attrs


class SubscriptionCreateSerializer(SubscriptionSerializer):
    """Serializer for creating subscription (organization comes from URL)."""

    class Meta(SubscriptionSerializer.Meta):
        read_only_fields = ['subscriptionId',
                            'organizationId', 'createdAt', 'updatedAt']


class SubscriptionUpdateSerializer(SubscriptionSerializer):
    """Serializer for updating subscription."""

    class Meta(SubscriptionSerializer.Meta):
        read_only_fields = ['subscriptionId', 'organizationId',
                            'productId', 'startDate', 'createdAt', 'updatedAt']
