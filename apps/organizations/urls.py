"""
Organization URL configuration for the headless SaaS platform.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.organizations.views import OrganizationViewSet, SubscriptionViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')

# URL patterns
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/organizations/<uuid:organization_id>/subscriptions/',
         SubscriptionViewSet.as_view({
             'get': 'list',
             'post': 'create',
         }), name='organization-subscriptions'),
    path('api/v1/organizations/<uuid:organization_id>/subscriptions/<uuid:pk>/',
         SubscriptionViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy',
         }), name='organization-subscription-detail'),
]
