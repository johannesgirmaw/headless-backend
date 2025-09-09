"""
Organization views for the headless SaaS platform.
Handles CRUD operations for Organization model.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from apps.organizations.models import Organization
from apps.organizations.serializers import (
    OrganizationSerializer,
    OrganizationCreateSerializer,
    OrganizationUpdateSerializer,
    OrganizationListSerializer,
    OrganizationDetailSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Organization CRUD operations.

    Provides:
    - List all organizations (with filtering and pagination)
    - Create new organization
    - Retrieve organization details
    - Update organization
    - Delete organization (soft delete)
    - Custom actions for organization management
    """

    queryset = Organization.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'status',
        'is_active',
        'timezone',
        'language',
        'currency',
        'account',
    ]
    search_fields = [
        'organization_id',
        'name',
        'organization_name',
        'organization_email',
        'city',
        'state',
        'country',
    ]
    ordering_fields = [
        'created_at',
        'updated_at',
        'organization_name',
        'status',
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return OrganizationListSerializer
        elif self.action == 'retrieve':
            return OrganizationDetailSerializer
        elif self.action == 'create':
            return OrganizationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrganizationUpdateSerializer
        return OrganizationSerializer

    def get_queryset(self):
        """Return filtered queryset based on user permissions."""
        queryset = super().get_queryset()

        # Filter by account if specified
        account_id = self.request.query_params.get('account')
        if account_id:
            queryset = queryset.filter(account_id=account_id)

        # For now, return all organizations (will be restricted based on user permissions later)
        # TODO: Implement proper multi-tenant filtering
        return queryset

    def perform_create(self, serializer):
        """Set the created_by field when creating a new organization."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field when updating an organization."""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Perform soft delete instead of hard delete."""
        instance.soft_delete(user=self.request.user)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate an organization."""
        organization = self.get_object()
        organization.is_active = True
        organization.status = 'active'
        organization.save(update_fields=['is_active', 'status'])

        serializer = self.get_serializer(organization)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate an organization."""
        organization = self.get_object()
        organization.is_active = False
        organization.status = 'inactive'
        organization.save(update_fields=['is_active', 'status'])

        serializer = self.get_serializer(organization)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Suspend an organization."""
        organization = self.get_object()
        organization.status = 'suspended'
        organization.save(update_fields=['status'])

        serializer = self.get_serializer(organization)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted organization."""
        organization = self.get_object()
        organization.restore(user=request.user)

        serializer = self.get_serializer(organization)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Get all users for this organization."""
        organization = self.get_object()
        users = organization.users.filter(deleted_at__isnull=True)

        # TODO: Implement user serializer
        return Response({
            'count': users.count(),
            'users': []  # Will be implemented when we create user serializers
        })

    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """Get all teams for this organization."""
        organization = self.get_object()
        teams = organization.teams.filter(deleted_at__isnull=True)

        # TODO: Implement team serializer
        return Response({
            'count': teams.count(),
            'teams': []  # Will be implemented when we create team serializers
        })

    @action(detail=True, methods=['post'])
    def set_feature(self, request, pk=None):
        """Set a feature flag for the organization."""
        organization = self.get_object()
        feature_name = request.data.get('feature_name')
        feature_value = request.data.get('feature_value')

        if not feature_name:
            return Response(
                {'error': 'feature_name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        organization.set_feature(feature_name, feature_value)

        serializer = self.get_serializer(organization)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_feature(self, request, pk=None):
        """Get a feature flag value for the organization."""
        organization = self.get_object()
        feature_name = request.query_params.get('feature_name')

        if not feature_name:
            return Response(
                {'error': 'feature_name query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        feature_value = organization.get_feature(feature_name)

        return Response({
            'feature_name': feature_name,
            'feature_value': feature_value
        })

    @action(detail=True, methods=['get'])
    def limits(self, request, pk=None):
        """Get organization limits and current usage."""
        organization = self.get_object()

        return Response({
            'max_users': organization.max_users,
            'current_users': organization.get_user_count(),
            'can_add_user': organization.can_add_user(),
            'max_teams': organization.max_teams,
            'current_teams': organization.get_team_count(),
            'can_add_team': organization.can_add_team(),
            'max_storage_gb': organization.max_storage_gb,
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get organization statistics."""
        queryset = self.get_queryset()
        total_organizations = queryset.count()
        active_organizations = queryset.filter(is_active=True).count()
        inactive_organizations = queryset.filter(is_active=False).count()
        suspended_organizations = queryset.filter(status='suspended').count()

        return Response({
            'total_organizations': total_organizations,
            'active_organizations': active_organizations,
            'inactive_organizations': inactive_organizations,
            'suspended_organizations': suspended_organizations,
        })
