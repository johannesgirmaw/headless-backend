"""
User models for the headless SaaS platform.
Custom user model that extends Django's AbstractUser.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from apps.accounts.models import Account
from apps.organizations.models import Organization


class UserManager(BaseUserManager):
    """Custom user manager for the User model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Users belong to organizations within accounts.
    """

    # Remove username field and use email as the unique identifier
    username = None
    email = models.EmailField(unique=True)

    # User identification
    user_id = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_-]+$',
            message='User ID can only contain letters, numbers, underscores, and hyphens.'
        )],
        help_text="Unique identifier for the user"
    )

    # Personal information
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    # Organization and account relationships
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

    # User settings
    timezone = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    date_format = models.CharField(max_length=20, default='MM/DD/YYYY')
    time_format = models.CharField(max_length=10, default='12h')

    # User status and permissions
    is_verified = models.BooleanField(default=False)
    is_organization_admin = models.BooleanField(default=False)
    is_account_admin = models.BooleanField(default=False)

    # User preferences
    preferences = models.JSONField(default=dict, blank=True)

    # Timestamps
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_location = models.CharField(
        max_length=255, blank=True, null=True)

    # Set email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id', 'first_name', 'last_name']

    # Custom manager
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def display_name(self):
        """Return the user's display name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    @property
    def effective_timezone(self):
        """Return user timezone or fallback to organization/account timezone."""
        return self.timezone or self.organization.effective_timezone

    @property
    def effective_language(self):
        """Return user language or fallback to organization/account language."""
        return self.language or self.organization.effective_language

    def get_preference(self, preference_name, default=None):
        """Get a user preference value."""
        return self.preferences.get(preference_name, default)

    def set_preference(self, preference_name, value):
        """Set a user preference value."""
        if not self.preferences:
            self.preferences = {}
        self.preferences[preference_name] = value
        self.save(update_fields=['preferences'])

    def can_manage_organization(self):
        """Check if user can manage the organization."""
        return self.is_organization_admin or self.is_account_admin

    def can_manage_account(self):
        """Check if user can manage the account."""
        return self.is_account_admin

    def get_accessible_organizations(self):
        """Get organizations the user can access."""
        if self.is_account_admin:
            return self.account.organizations.filter(deleted_at__isnull=True)
        return Organization.objects.filter(id=self.organization.id, deleted_at__isnull=True)
