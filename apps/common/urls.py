"""
Health check and monitoring URLs.
"""

from django.urls import path
from apps.common.monitoring import HealthCheckView, MetricsView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
]
