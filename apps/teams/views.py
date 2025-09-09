"""
Team views for the headless SaaS platform.
Handles CRUD operations for Team and TeamMember models.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from apps.teams.models import Team, TeamMember
from apps.teams.serializers import (
    TeamSerializer,
    TeamCreateSerializer,
    TeamUpdateSerializer,
    TeamListSerializer,
    TeamDetailSerializer,
    TeamMemberSerializer,
    TeamMemberCreateSerializer,
    TeamMemberUpdateSerializer,
    TeamMemberListSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team CRUD operations.
    """

    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'status',
        'is_active',
        'team_type',
        'account',
        'organization',
    ]
    search_fields = [
        'team_id',
        'name',
        'team_name',
        'team_email',
    ]
    ordering_fields = [
        'created_at',
        'updated_at',
        'team_name',
        'status',
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return TeamListSerializer
        elif self.action == 'retrieve':
            return TeamDetailSerializer
        elif self.action == 'create':
            return TeamCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TeamUpdateSerializer
        return TeamSerializer

    def get_queryset(self):
        """Return filtered queryset based on user permissions."""
        queryset = super().get_queryset()

        # Filter by account if specified
        account_id = self.request.query_params.get('account')
        if account_id:
            queryset = queryset.filter(account_id=account_id)

        # Filter by organization if specified
        organization_id = self.request.query_params.get('organization')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)

        return queryset

    def perform_create(self, serializer):
        """Set the created_by field when creating a new team."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field when updating a team."""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Perform soft delete instead of hard delete."""
        instance.soft_delete(user=self.request.user)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a team."""
        team = self.get_object()
        team.is_active = True
        team.status = 'active'
        team.save(update_fields=['is_active', 'status'])

        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a team."""
        team = self.get_object()
        team.is_active = False
        team.status = 'inactive'
        team.save(update_fields=['is_active', 'status'])

        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted team."""
        team = self.get_object()
        team.restore(user=request.user)

        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members for this team."""
        team = self.get_object()
        members = team.members.all()

        serializer = TeamMemberListSerializer(members, many=True)
        return Response({
            'count': members.count(),
            'members': serializer.data
        })

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team."""
        team = self.get_object()

        if not team.can_add_member():
            return Response(
                {'error': 'Team has reached maximum member limit'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')

        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from apps.users.models import User
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user is already a member
        if TeamMember.objects.filter(team=team, user=user).exists():
            return Response(
                {'error': 'User is already a member of this team'},
                status=status.HTTP_400_BAD_REQUEST
            )

        member = TeamMember.objects.create(
            team=team,
            user=user,
            role=role,
            created_by=request.user
        )

        serializer = TeamMemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TeamMember CRUD operations.
    """

    queryset = TeamMember.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'role',
        'status',
        'team',
        'user',
    ]
    search_fields = [
        'user__user_id',
        'user__email',
        'user__first_name',
        'user__last_name',
    ]
    ordering_fields = [
        'created_at',
        'updated_at',
        'user__last_name',
        'user__first_name',
        'role',
    ]
    ordering = ['user__last_name', 'user__first_name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return TeamMemberListSerializer
        elif self.action == 'create':
            return TeamMemberCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TeamMemberUpdateSerializer
        return TeamMemberSerializer

    def get_queryset(self):
        """Return filtered queryset based on user permissions."""
        queryset = super().get_queryset()

        # Filter by team if specified
        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = queryset.filter(team_id=team_id)

        # Filter by user if specified
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        """Set the created_by field when creating a new team member."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field when updating a team member."""
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        """Change team member role."""
        member = self.get_object()
        new_role = request.data.get('role')

        if not new_role:
            return Response(
                {'error': 'role is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_roles = ['owner', 'admin', 'member', 'viewer']
        if new_role not in valid_roles:
            return Response(
                {'error': f'Role must be one of: {", ".join(valid_roles)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        member.role = new_role
        member.save(update_fields=['role'])

        serializer = self.get_serializer(member)
        return Response(serializer.data)
