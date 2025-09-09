
"""
Account views for the headless SaaS platform.
Handles CRUD operations for Account model.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from apps.accounts.models import Account
from apps.accounts.serializers import (
    AccountSerializer,
    AccountCreateSerializer,
    AccountUpdateSerializer,
    AccountListSerializer,
    AccountDetailSerializer,
)


class AccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Account CRUD operations.

    Provides:
    - List all accounts (with filtering and pagination)
    - Create new account
    - Retrieve account details
    - Update account
    - Delete account (soft delete)
    - Custom actions for account management
    """

    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'subscription_status',
        'subscription_plan',
        'is_active',
        'timezone',
        'language',
        'currency',
    ]
    search_fields = [
        'account_id',
        'name',
        'company_name',
        'company_email',
        'city',
        'state',
        'country',
    ]
    ordering_fields = [
        'created_at',
        'updated_at',
        'company_name',
        'subscription_status',
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AccountListSerializer
        elif self.action == 'retrieve':
            return AccountDetailSerializer
        elif self.action == 'create':
            return AccountCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AccountUpdateSerializer
        return AccountSerializer

    def get_queryset(self):
        """Return filtered queryset based on user permissions."""
        queryset = super().get_queryset()

        # For now, return all accounts (will be restricted based on user permissions later)
        # TODO: Implement proper multi-tenant filtering
        return queryset

    def perform_create(self, serializer):
        """Set the created_by field when creating a new account."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field when updating an account."""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Perform soft delete instead of hard delete."""
        instance.soft_delete(user=self.request.user)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate an account."""
        account = self.get_object()
        account.is_active = True
        account.save(update_fields=['is_active'])

        serializer = self.get_serializer(account)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate an account."""
        account = self.get_object()
        account.is_active = False
        account.save(update_fields=['is_active'])

        serializer = self.get_serializer(account)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted account."""
        account = self.get_object()
        account.restore(user=request.user)

        serializer = self.get_serializer(account)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def organizations(self, request, pk=None):
        """Get all organizations for this account."""
        account = self.get_object()
        organizations = account.organizations.filter(deleted_at__isnull=True)

        # TODO: Implement organization serializer
        return Response({
            'count': organizations.count(),
            'organizations': []  # Will be implemented when we create organization serializers
        })

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Get all users for this account."""
        account = self.get_object()
        users = account.users.filter(deleted_at__isnull=True)

        # TODO: Implement user serializer
        return Response({
            'count': users.count(),
            'users': []  # Will be implemented when we create user serializers
        })

    @action(detail=True, methods=['post'])
    def set_feature(self, request, pk=None):
        """Set a feature flag for the account."""
        account = self.get_object()
        feature_name = request.data.get('feature_name')
        feature_value = request.data.get('feature_value')

        if not feature_name:
            return Response(
                {'error': 'feature_name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        account.set_feature(feature_name, feature_value)

        serializer = self.get_serializer(account)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_feature(self, request, pk=None):
        """Get a feature flag value for the account."""
        account = self.get_object()
        feature_name = request.query_params.get('feature_name')

        if not feature_name:
            return Response(
                {'error': 'feature_name query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        feature_value = account.get_feature(feature_name)

        return Response({
            'feature_name': feature_name,
            'feature_value': feature_value
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get account statistics."""
        total_accounts = self.get_queryset().count()
        active_accounts = self.get_queryset().filter(is_active=True).count()
        trial_accounts = self.get_queryset().filter(subscription_status='trial').count()
        active_subscriptions = self.get_queryset().filter(
            subscription_status='active').count()

        return Response({
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'trial_accounts': trial_accounts,
            'active_subscriptions': active_subscriptions,
        })
