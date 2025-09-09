"""
Common app URLs including health checks, monitoring, and RBAC.
"""

from django.urls import path, include
from apps.common.monitoring import HealthCheckView, MetricsView

urlpatterns = [
    # Health check and monitoring
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('metrics/', MetricsView.as_view(), name='metrics'),

    # RBAC (Role-Based Access Control)
    path('', include('apps.common.rbac_urls')),
]
