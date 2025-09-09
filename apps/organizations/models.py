"""
Organization models for the headless SaaS platform.
Organizations belong to accounts and contain users and teams.
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.common.models import BaseModel
from apps.accounts.models import Account


class Organization(BaseModel):
    """
    Organization model representing a department or division within an account.
    Each organization can have multiple users and teams.
    """

    # Organization identification
    organization_id = models.CharField(
        max_length=50,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_-]+$',
            message='Organization ID can only contain letters, numbers, underscores, and hyphens.'
        )],
        help_text="Unique identifier for the organization within the account"
    )

    # Parent account
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='organizations'
    )

    # Organization details
    organization_name = models.CharField(max_length=255)
    organization_email = models.EmailField(blank=True, null=True)
    organization_phone = models.CharField(max_length=20, blank=True, null=True)
    organization_website = models.URLField(blank=True, null=True)

    # Address information (can inherit from account or be different)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Organization settings
    timezone = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)

    # Organization limits
    max_users = models.PositiveIntegerField(default=10)
    max_teams = models.PositiveIntegerField(default=5)
    max_storage_gb = models.PositiveIntegerField(default=1)

    # Organization features
    features = models.JSONField(default=dict, blank=True)

    # Organization status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended'),
        ],
        default='active'
    )

    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['organization_name']
        unique_together = ['account', 'organization_id']

    def __str__(self):
        return f"{self.organization_name} ({self.account.company_name})"

    @property
    def full_address(self):
        """Return the complete address as a string."""
        address_parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, address_parts))

    @property
    def effective_timezone(self):
        """Return organization timezone or fallback to account timezone."""
        return self.timezone or self.account.timezone

    @property
    def effective_language(self):
        """Return organization language or fallback to account language."""
        return self.language or self.account.language

    @property
    def effective_currency(self):
        """Return organization currency or fallback to account currency."""
        return self.currency or self.account.currency

    def get_feature(self, feature_name, default=False):
        """Get a feature flag value."""
        return self.features.get(feature_name, default)

    def set_feature(self, feature_name, value):
        """Set a feature flag value."""
        if not self.features:
            self.features = {}
        self.features[feature_name] = value
        self.save(update_fields=['features'])

    def get_user_count(self):
        """Get the current number of users in this organization."""
        return self.users.count()

    def get_team_count(self):
        """Get the current number of teams in this organization."""
        return self.teams.count()

    def can_add_user(self):
        """Check if a new user can be added to this organization."""
        return self.get_user_count() < self.max_users

    def can_add_team(self):
        """Check if a new team can be added to this organization."""
        return self.get_team_count() < self.max_teams


class Subscription(BaseModel):
    """
    Subscription for an organization to a product.
    Tracks lifecycle and plan configuration.
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    ]

    # Parent organization
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    # Product reference (external/catalog id)
    product_id = models.PositiveIntegerField()

    # Dates
    start_date = models.DateField()
    end_date = models.DateField()

    # Status and configuration
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')
    plan_configuration = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'organization_subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Subscription {self.product_id} for {self.organization.organization_name} ({self.status})"
