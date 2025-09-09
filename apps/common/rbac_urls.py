from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .rbac_views import (
    PermissionViewSet, RoleViewSet, UserGroupViewSet,
    UserRBACViewSet, SystemRoleViewSet
)

# Create router for RBAC viewsets
router = DefaultRouter()
router.register(r'permissions', PermissionViewSet, basename='permissions')
router.register(r'system-roles', SystemRoleViewSet, basename='system-roles')

# Organization-scoped RBAC URLs
organization_router = DefaultRouter()
organization_router.register(
    r'roles', RoleViewSet, basename='organization-roles')
organization_router.register(
    r'groups', UserGroupViewSet, basename='organization-groups')
organization_router.register(
    r'users', UserRBACViewSet, basename='organization-users')

urlpatterns = [
    # Global RBAC endpoints
    path('rbac/', include(router.urls)),

    # Organization-scoped RBAC endpoints
    path('organizations/<uuid:organization_id>/rbac/',
         include(organization_router.urls)),
]
