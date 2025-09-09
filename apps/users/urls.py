"""
User URL configuration for the headless SaaS platform.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import UserViewSet
from apps.users.auth_views import (
    CustomTokenObtainPairView,
    register_view,
    logout_view,
    me_view,
    change_password_view,
    verify_email_view,
    forgot_password_view,
    reset_password_view,
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# URL patterns
urlpatterns = [
    path('api/v1/', include(router.urls)),

    # Authentication URLs
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/register/', register_view, name='register'),
    path('api/v1/auth/logout/', logout_view, name='logout'),
    path('api/v1/auth/me/', me_view, name='me'),
    path('api/v1/auth/change-password/',
         change_password_view, name='change_password'),
    path('api/v1/auth/verify-email/', verify_email_view, name='verify_email'),
    path('api/v1/auth/forgot-password/',
         forgot_password_view, name='forgot_password'),
    path('api/v1/auth/reset-password/',
         reset_password_view, name='reset_password'),
]
