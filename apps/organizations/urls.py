"""
Organization URL configuration for the headless SaaS platform.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.organizations.views import OrganizationViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')

# URL patterns
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
