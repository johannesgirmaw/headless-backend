"""
Team serializers for the headless SaaS platform.
Handles serialization and validation of Team and TeamMember data.
"""

from rest_framework import serializers
from apps.teams.models import Team, TeamMember
from apps.accounts.models import Account
from apps.organizations.models import Organization
from apps.users.models import User


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""

    # Computed fields
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id',
            'team_id',
            'name',
            'description',
            'is_active',
            'account',
            'organization',
            'team_name',
            'team_email',
            'team_phone',
            'team_website',
            'team_type',
            'max_members',
            'member_count',
            'features',
            'status',
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
            'member_count',
        ]

    def validate_team_id(self, value):
        """Validate team_id uniqueness within organization."""
        organization_id = self.initial_data.get('organization')
        if not organization_id:
            raise serializers.ValidationError("Organization is required.")

        if self.instance and self.instance.team_id == value:
            return value

        if Team.objects.filter(
            organization_id=organization_id,
            team_id=value
        ).exists():
            raise serializers.ValidationError(
                "A team with this ID already exists in this organization."
            )
        return value

    def validate_team_email(self, value):
        """Validate team email uniqueness within organization."""
        organization_id = self.initial_data.get('organization')
        if not value or not organization_id:
            return value

        if self.instance and self.instance.team_email == value:
            return value

        if Team.objects.filter(
            organization_id=organization_id,
            team_email=value
        ).exists():
            raise serializers.ValidationError(
                "A team with this email already exists in this organization."
            )
        return value

    def validate_max_members(self, value):
        """Validate max_members is reasonable."""
        if value <= 0:
            raise serializers.ValidationError(
                "Max members must be greater than 0."
            )
        if value > 1000:
            raise serializers.ValidationError(
                "Max members cannot exceed 1000."
            )
        return value

    def get_member_count(self, obj):
        """Get the current number of members in this team."""
        return obj.get_member_count()


class TeamCreateSerializer(TeamSerializer):
    """Serializer for creating new teams."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields
        read_only_fields = TeamSerializer.Meta.read_only_fields


class TeamUpdateSerializer(TeamSerializer):
    """Serializer for updating existing teams."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields
        read_only_fields = TeamSerializer.Meta.read_only_fields + [
            'team_id',  # Team ID cannot be changed after creation
            'account',  # Account cannot be changed after creation
            'organization',  # Organization cannot be changed after creation
        ]


class TeamListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for team lists."""

    member_count = serializers.SerializerMethodField()
    account_name = serializers.CharField(
        source='account.company_name', read_only=True)
    organization_name = serializers.CharField(
        source='organization.organization_name', read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'team_id',
            'name',
            'team_name',
            'team_email',
            'account_name',
            'organization_name',
            'team_type',
            'max_members',
            'member_count',
            'status',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_member_count(self, obj):
        """Get the current number of members in this team."""
        return obj.get_member_count()


class TeamDetailSerializer(TeamSerializer):
    """Detailed serializer for team details."""

    # Add related data
    account_details = serializers.SerializerMethodField()
    organization_details = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + [
            'account_details',
            'organization_details',
            'members',
        ]

    def get_account_details(self, obj):
        """Get account details."""
        return {
            'id': obj.account.id,
            'account_id': obj.account.account_id,
            'company_name': obj.account.company_name,
            'company_email': obj.account.company_email,
        }

    def get_organization_details(self, obj):
        """Get organization details."""
        return {
            'id': obj.organization.id,
            'organization_id': obj.organization.organization_id,
            'organization_name': obj.organization.organization_name,
            'organization_email': obj.organization.organization_email,
        }

    def get_members(self, obj):
        """Get team members."""
        members = obj.members.all()
        return TeamMemberSerializer(members, many=True).data


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model."""

    user_details = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'team',
            'user',
            'user_details',
            'role',
            'status',
            'permissions',
            'settings',
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
            'user_details',
        ]

    def validate_role(self, value):
        """Validate role value."""
        valid_roles = ['owner', 'admin', 'member', 'viewer']
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Role must be one of: {', '.join(valid_roles)}"
            )
        return value

    def validate_status(self, value):
        """Validate status value."""
        valid_statuses = ['active', 'inactive', 'pending']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value

    def get_user_details(self, obj):
        """Get user details."""
        return {
            'id': obj.user.id,
            'user_id': obj.user.user_id,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'display_name': obj.user.display_name,
            'avatar': obj.user.avatar,
        }


class TeamMemberCreateSerializer(TeamMemberSerializer):
    """Serializer for creating new team members."""

    class Meta(TeamMemberSerializer.Meta):
        fields = TeamMemberSerializer.Meta.fields
        read_only_fields = TeamMemberSerializer.Meta.read_only_fields


class TeamMemberUpdateSerializer(TeamMemberSerializer):
    """Serializer for updating existing team members."""

    class Meta(TeamMemberSerializer.Meta):
        fields = TeamMemberSerializer.Meta.fields
        read_only_fields = TeamMemberSerializer.Meta.read_only_fields + [
            'team',  # Team cannot be changed after creation
            'user',  # User cannot be changed after creation
        ]


class TeamMemberListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for team member lists."""

    user_details = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'user_details',
            'role',
            'status',
            'created_at',
            'updated_at',
        ]

    def get_user_details(self, obj):
        """Get user details."""
        return {
            'id': obj.user.id,
            'user_id': obj.user.user_id,
            'email': obj.user.email,
            'display_name': obj.user.display_name,
            'avatar': obj.user.avatar,
        }
