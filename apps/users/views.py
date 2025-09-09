"""
User views for the headless SaaS platform.
Handles CRUD operations for User model.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import authenticate
from django.db.models import Q

from apps.users.models import User
from apps.users.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations.

    Provides:
    - List all users (with filtering and pagination)
    - Create new user
    - Retrieve user details
    - Update user
    - Delete user (soft delete)
    - Custom actions for user management
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'is_active',
        'is_verified',
        'is_organization_admin',
        'is_account_admin',
        'account',
        'organization',
        'timezone',
        'language',
    ]
    search_fields = [
        'user_id',
        'email',
        'first_name',
        'last_name',
        'phone',
    ]
    ordering_fields = [
        'created_at',
        'updated_at',
        'last_name',
        'first_name',
        'last_login',
        'date_joined',
    ]
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

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

        # For now, return all users (will be restricted based on user permissions later)
        # TODO: Implement proper multi-tenant filtering
        return queryset

    def perform_create(self, serializer):
        """Set the created_by field when creating a new user."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field when updating a user."""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Perform soft delete instead of hard delete."""
        # Note: User model doesn't inherit from SoftDeleteModel, so we'll just deactivate
        instance.is_active = False
        instance.save(update_fields=['is_active'])

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a user."""
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a user."""
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=['is_active'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a user."""
        user = self.get_object()
        user.is_verified = True
        user.save(update_fields=['is_verified'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def make_organization_admin(self, request, pk=None):
        """Make user an organization admin."""
        user = self.get_object()
        user.is_organization_admin = True
        user.save(update_fields=['is_organization_admin'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def make_account_admin(self, request, pk=None):
        """Make user an account admin."""
        user = self.get_object()
        user.is_account_admin = True
        user.save(update_fields=['is_account_admin'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Change user password."""
        user = self.get_object()
        serializer = UserPasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password changed successfully'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """Get all teams for this user."""
        user = self.get_object()
        team_memberships = user.team_memberships.all()

        # TODO: Implement team serializer
        return Response({
            'count': team_memberships.count(),
            'teams': []  # Will be implemented when we create team serializers
        })

    @action(detail=True, methods=['post'])
    def set_preference(self, request, pk=None):
        """Set a user preference."""
        user = self.get_object()
        preference_name = request.data.get('preference_name')
        preference_value = request.data.get('preference_value')

        if not preference_name:
            return Response(
                {'error': 'preference_name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_preference(preference_name, preference_value)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_preference(self, request, pk=None):
        """Get a user preference value."""
        user = self.get_object()
        preference_name = request.query_params.get('preference_name')

        if not preference_name:
            return Response(
                {'error': 'preference_name query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        preference_value = user.get_preference(preference_name)

        return Response({
            'preference_name': preference_name,
            'preference_value': preference_value
        })

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login endpoint."""
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user details."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_my_password(self, request):
        """Change current user's password."""
        serializer = UserPasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password changed successfully'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics."""
        queryset = self.get_queryset()
        total_users = queryset.count()
        active_users = queryset.filter(is_active=True).count()
        verified_users = queryset.filter(is_verified=True).count()
        organization_admins = queryset.filter(
            is_organization_admin=True).count()
        account_admins = queryset.filter(is_account_admin=True).count()

        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'organization_admins': organization_admins,
            'account_admins': account_admins,
        })
