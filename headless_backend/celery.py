"""
Celery configuration for headless_backend project.
"""

import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'headless_backend.settings_production')

app = Celery('headless_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'send-email-verification-reminders': {
        'task': 'apps.users.tasks.send_email_verification_reminders',
        'schedule': 86400.0,  # Run daily
    },
    'cleanup-expired-tokens': {
        'task': 'apps.users.tasks.cleanup_expired_tokens',
        'schedule': 3600.0,  # Run hourly
    },
    'generate-monthly-reports': {
        'task': 'apps.accounts.tasks.generate_monthly_reports',
        'schedule': 2592000.0,  # Run monthly
    },
    'backup-database': {
        'task': 'apps.common.tasks.backup_database',
        'schedule': 86400.0,  # Run daily
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
