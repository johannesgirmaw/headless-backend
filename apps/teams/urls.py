"""
Team URL configuration for the headless SaaS platform.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.teams.views import TeamViewSet, TeamMemberViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'team-members', TeamMemberViewSet, basename='team-member')

# URL patterns
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
