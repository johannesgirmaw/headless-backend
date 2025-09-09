"""
Account models for the headless SaaS platform.
Accounts represent the top-level tenant in the multi-tenant architecture.
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.common.models import BaseModel


class Account(BaseModel):
    """
    Account model representing the top-level tenant.
    Each account can have multiple organizations.
    """

    # Account identification
    account_id = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_-]+$',
            message='Account ID can only contain letters, numbers, underscores, and hyphens.'
        )],
        help_text="Unique identifier for the account (used in URLs)"
    )

    # Account details
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)

    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Account settings
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    currency = models.CharField(max_length=3, default='USD')

    # Subscription and billing
    subscription_plan = models.CharField(max_length=50, default='free')
    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('cancelled', 'Cancelled'),
            ('trial', 'Trial'),
        ],
        default='trial'
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)

    # Account limits and usage
    max_organizations = models.PositiveIntegerField(default=1)
    max_users_per_organization = models.PositiveIntegerField(default=10)
    max_storage_gb = models.PositiveIntegerField(default=1)

    # Feature flags
    features = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['company_name']

    def __str__(self):
        return f"{self.company_name} ({self.account_id})"

    @property
    def is_subscription_active(self):
        """Check if the account's subscription is active."""
        if self.subscription_status == 'active':
            return True
        elif self.subscription_status == 'trial':
            return True
        return False

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

    def get_feature(self, feature_name, default=False):
        """Get a feature flag value."""
        return self.features.get(feature_name, default)

    def set_feature(self, feature_name, value):
        """Set a feature flag value."""
        if not self.features:
            self.features = {}
        self.features[feature_name] = value
        self.save(update_fields=['features'])
