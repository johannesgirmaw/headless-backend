from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .rbac_models import (
    Permission, Role, UserGroup, RolePermission, UserRole,
    UserPermission, GroupPermission, UserGroupMembership, RoleGroup
)
from .rbac_serializers import (
    PermissionSerializer, PermissionListSerializer,
    RoleSerializer, RoleListSerializer, RolePermissionSerializer,
    UserGroupSerializer, UserGroupListSerializer, UserGroupMembershipSerializer,
    UserRoleSerializer, UserPermissionSerializer, GroupPermissionSerializer,
    RoleGroupSerializer, UserRBACSerializer, AssignRoleSerializer,
    AssignPermissionSerializer, AddToGroupSerializer
)
from .rbac_permissions import RBACPermission, ModelRBACPermission, OrganizationPermission
from .rbac_manager import get_rbac_manager

User = get_user_model()


class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing permissions."""

    queryset = Permission.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, RBACPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return PermissionListSerializer
        return PermissionSerializer

    def get_permissions(self):
        """Return instantiated permissions, not classes with parameters."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), RBACPermission(['permissions_read'])]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), RBACPermission([
                'permissions_create', 'permissions_update'
            ])]
        elif self.action == 'destroy':
            return [IsAuthenticated(), RBACPermission(['permissions_delete'])]
        return [perm() for perm in self.permission_classes]

    def get_queryset(self):
        """Filter permissions by model if specified."""
        queryset = super().get_queryset()
        model_name = self.request.query_params.get('model_name')
        if model_name:
            queryset = queryset.filter(model_name=model_name)
        return queryset


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing roles."""

    queryset = Role.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, OrganizationPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer

    def get_permissions(self):
        """Return instantiated permissions for organization-scoped checks."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), OrganizationPermission(['roles_read'])]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), OrganizationPermission([
                'roles_create', 'roles_update'
            ])]
        elif self.action == 'destroy':
            return [IsAuthenticated(), OrganizationPermission(['roles_delete'])]
        return [perm() for perm in self.permission_classes]

    def get_queryset(self):
        """Filter roles by organization."""
        queryset = super().get_queryset()
        organization_id = self.kwargs.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

    @action(detail=True, methods=['post'], url_path='assign-permissions')
    def assign_permissions(self, request, pk=None, organization_id=None):
        """Assign permissions to a role."""
        role = self.get_object()
        serializer = AssignPermissionSerializer(data=request.data)

        if serializer.is_valid():
            permission_ids = serializer.validated_data['permission_ids']
            expires_at = serializer.validated_data.get('expires_at')

            with transaction.atomic():
                # Remove existing permissions
                RolePermission.objects.filter(role=role).delete()

                # Add new permissions
                for permission_id in permission_ids:
                    RolePermission.objects.create(
                        role=role,
                        permission_id=permission_id,
                        granted_by=request.user,
                        expires_at=expires_at
                    )

            return Response({'message': 'Permissions assigned successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='permissions')
    def list_role_permissions(self, request, pk=None, organization_id=None):
        """Get permissions assigned to a role."""
        role = self.get_object()
        permissions = role.role_permissions.filter(permission__is_active=True)
        serializer = RolePermissionSerializer(permissions, many=True)
        return Response(serializer.data)


class UserGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user groups."""

    queryset = UserGroup.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, OrganizationPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserGroupListSerializer
        return UserGroupSerializer

    def get_permissions(self):
        """Return instantiated permissions for organization-scoped checks."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), OrganizationPermission(['groups_read'])]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), OrganizationPermission([
                'groups_create', 'groups_update'
            ])]
        elif self.action == 'destroy':
            return [IsAuthenticated(), OrganizationPermission(['groups_delete'])]
        return [perm() for perm in self.permission_classes]

    def get_queryset(self):
        """Filter groups by organization."""
        queryset = super().get_queryset()
        organization_id = self.kwargs.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-members')
    def add_members(self, request, pk=None, organization_id=None):
        """Add users to a group."""
        group = self.get_object()
        serializer = AddToGroupSerializer(data=request.data)

        if serializer.is_valid():
            user_ids = serializer.validated_data['user_ids']
            expires_at = serializer.validated_data.get('expires_at')

            with transaction.atomic():
                for user_id in user_ids:
                    UserGroupMembership.objects.update_or_create(
                        user_id=user_id,
                        group=group,
                        defaults={
                            'added_by': request.user,
                            'expires_at': expires_at,
                            'is_active': True
                        }
                    )

            return Response({'message': 'Members added successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove-members')
    def remove_members(self, request, pk=None, organization_id=None):
        """Remove users from a group."""
        group = self.get_object()
        user_ids = request.data.get('user_ids', [])

        if not user_ids:
            return Response({'error': 'user_ids is required'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            UserGroupMembership.objects.filter(
                group=group,
                user_id__in=user_ids
            ).update(is_active=False)

        return Response({'message': 'Members removed successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='members')
    def get_members(self, request, pk=None, organization_id=None):
        """Get members of a group."""
        group = self.get_object()
        memberships = group.group_memberships.filter(is_active=True)
        serializer = UserGroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='assign-roles')
    def assign_roles(self, request, pk=None, organization_id=None):
        """Assign roles to a group."""
        group = self.get_object()
        serializer = AssignRoleSerializer(data=request.data)

        if serializer.is_valid():
            role_ids = serializer.validated_data['role_ids']
            expires_at = serializer.validated_data.get('expires_at')

            with transaction.atomic():
                # Remove existing roles
                RoleGroup.objects.filter(group=group).delete()

                # Add new roles
                for role_id in role_ids:
                    RoleGroup.objects.create(
                        group=group,
                        role_id=role_id,
                        assigned_by=request.user,
                        expires_at=expires_at
                    )

            return Response({'message': 'Roles assigned successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRBACViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user RBAC information."""

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRBACSerializer
    permission_classes = [IsAuthenticated, OrganizationPermission]

    def get_permissions(self):
        return [IsAuthenticated(), OrganizationPermission(['users_read'])]

    def get_queryset(self):
        """Filter users by organization."""
        queryset = super().get_queryset()
        organization_id = self.kwargs.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

    def get_serializer_context(self):
        """Add organization_id to context."""
        context = super().get_serializer_context()
        context['organization_id'] = self.kwargs.get('organization_id')
        return context

    @action(detail=True, methods=['post'], url_path='assign-roles')
    def assign_roles(self, request, pk=None, organization_id=None):
        """Assign roles to a user."""
        user = self.get_object()
        serializer = AssignRoleSerializer(data=request.data)

        if serializer.is_valid():
            role_ids = serializer.validated_data['role_ids']
            expires_at = serializer.validated_data.get('expires_at')

            with transaction.atomic():
                # Remove existing roles
                UserRole.objects.filter(user=user).delete()

                # Add new roles
                for role_id in role_ids:
                    UserRole.objects.create(
                        user=user,
                        role_id=role_id,
                        assigned_by=request.user,
                        expires_at=expires_at
                    )

            return Response({'message': 'Roles assigned successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='assign-permissions')
    def assign_permissions(self, request, pk=None, organization_id=None):
        """Assign direct permissions to a user."""
        user = self.get_object()
        serializer = AssignPermissionSerializer(data=request.data)

        if serializer.is_valid():
            permission_ids = serializer.validated_data['permission_ids']
            expires_at = serializer.validated_data.get('expires_at')

            with transaction.atomic():
                # Remove existing direct permissions
                UserPermission.objects.filter(user=user).delete()

                # Add new permissions
                for permission_id in permission_ids:
                    UserPermission.objects.create(
                        user=user,
                        permission_id=permission_id,
                        granted_by=request.user,
                        expires_at=expires_at
                    )

            return Response({'message': 'Permissions assigned successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='permissions')
    def get_user_permissions(self, request, pk=None, organization_id=None):
        """Get all permissions for a user."""
        user = self.get_object()
        rbac_manager = get_rbac_manager(user)
        permissions = rbac_manager.get_user_permissions(organization_id)

        return Response({
            'user_id': str(user.id),
            'email': user.email,
            'permissions': list(permissions)
        })

    @action(detail=True, methods=['get'], url_path='roles')
    def get_user_roles(self, request, pk=None, organization_id=None):
        """Get all roles for a user."""
        user = self.get_object()
        rbac_manager = get_rbac_manager(user)
        roles = rbac_manager.get_user_roles(organization_id)

        return Response({
            'user_id': str(user.id),
            'email': user.email,
            'roles': roles
        })

    @action(detail=True, methods=['get'], url_path='groups')
    def get_user_groups(self, request, pk=None, organization_id=None):
        """Get all groups for a user."""
        user = self.get_object()
        rbac_manager = get_rbac_manager(user)
        groups = rbac_manager.get_user_groups(organization_id)

        return Response({
            'user_id': str(user.id),
            'email': user.email,
            'groups': groups
        })


class SystemRoleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for system roles (read-only)."""

    queryset = Role.objects.filter(is_active=True, role_type='system')
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated, RBACPermission]

    def get_permissions(self):
        return [IsAuthenticated(), RBACPermission(['roles_read'])]

    @action(detail=True, methods=['get'], url_path='permissions')
    def list_role_permissions(self, request, pk=None):
        """Get permissions assigned to a system role."""
        role = self.get_object()
        permissions = role.role_permissions.filter(permission__is_active=True)
        serializer = RolePermissionSerializer(permissions, many=True)
        return Response(serializer.data)
