"""
Account URL configuration for the headless SaaS platform.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts.views import AccountViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')

# URL patterns
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
