"""
Team models for the headless SaaS platform.
Teams belong to organizations and contain users.
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.common.models import BaseModel
from apps.accounts.models import Account
from apps.organizations.models import Organization
from apps.users.models import User


class Team(BaseModel):
    """
    Team model representing a group of users within an organization.
    Teams can be used for project management, department organization, etc.
    """

    # Team identification
    team_id = models.CharField(
        max_length=50,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_-]+$',
            message='Team ID can only contain letters, numbers, underscores, and hyphens.'
        )],
        help_text="Unique identifier for the team within the organization"
    )

    # Parent relationships
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='teams'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='teams'
    )

    # Team details
    team_name = models.CharField(max_length=255)
    team_email = models.EmailField(blank=True, null=True)
    team_phone = models.CharField(max_length=20, blank=True, null=True)
    team_website = models.URLField(blank=True, null=True)

    # Team settings
    team_type = models.CharField(
        max_length=50,
        choices=[
            ('department', 'Department'),
            ('project', 'Project'),
            ('functional', 'Functional'),
            ('cross-functional', 'Cross-functional'),
            ('ad-hoc', 'Ad-hoc'),
        ],
        default='functional'
    )

    # Team limits
    max_members = models.PositiveIntegerField(default=20)

    # Team features
    features = models.JSONField(default=dict, blank=True)

    # Team status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('archived', 'Archived'),
        ],
        default='active'
    )

    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['team_name']
        unique_together = ['organization', 'team_id']

    def __str__(self):
        return f"{self.team_name} ({self.organization.organization_name})"

    def get_feature(self, feature_name, default=False):
        """Get a feature flag value."""
        return self.features.get(feature_name, default)

    def set_feature(self, feature_name, value):
        """Set a feature flag value."""
        if not self.features:
            self.features = {}
        self.features[feature_name] = value
        self.save(update_fields=['features'])

    def get_member_count(self):
        """Get the current number of members in this team."""
        return self.members.count()

    def can_add_member(self):
        """Check if a new member can be added to this team."""
        return self.get_member_count() < self.max_members

    def get_members(self):
        """Get all active members of this team."""
        return self.members.all()


class TeamMember(BaseModel):
    """
    Team member model representing the relationship between users and teams.
    Includes role and permission information for team members.
    """

    # Relationships
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='team_memberships'
    )

    # Member role and permissions
    role = models.CharField(
        max_length=50,
        choices=[
            ('owner', 'Owner'),
            ('admin', 'Admin'),
            ('member', 'Member'),
            ('viewer', 'Viewer'),
        ],
        default='member'
    )

    # Member status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('pending', 'Pending'),
        ],
        default='active'
    )

    # Member permissions
    permissions = models.JSONField(default=dict, blank=True)

    # Member settings
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'team_members'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        unique_together = ['team', 'user']
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.display_name} - {self.team.team_name} ({self.role})"

    def get_permission(self, permission_name, default=False):
        """Get a permission value."""
        return self.permissions.get(permission_name, default)

    def set_permission(self, permission_name, value):
        """Set a permission value."""
        if not self.permissions:
            self.permissions = {}
        self.permissions[permission_name] = value
        self.save(update_fields=['permissions'])

    def get_setting(self, setting_name, default=None):
        """Get a setting value."""
        return self.settings.get(setting_name, default)

    def set_setting(self, setting_name, value):
        """Set a setting value."""
        if not self.settings:
            self.settings = {}
        self.settings[setting_name] = value
        self.save(update_fields=['settings'])

    def can_manage_team(self):
        """Check if member can manage the team."""
        return self.role in ['owner', 'admin']

    def can_invite_members(self):
        """Check if member can invite new members."""
        return self.role in ['owner', 'admin']

    def can_remove_members(self):
        """Check if member can remove members."""
        return self.role == 'owner'
