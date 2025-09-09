"""
Django settings for headless_backend project.

Production-ready configuration with PostgreSQL, Redis, Email, File Storage,
Monitoring, Rate Limiting, and Caching.
"""

from datetime import timedelta
import os
from pathlib import Path
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables with comprehensive defaults
env = environ.Env(
    # Django Core
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'django-insecure-change-me'),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),

    # Database
    DATABASE_URL=(str, 'sqlite:///db.sqlite3'),
    DB_NAME=(str, 'headless_backend_db'),
    DB_USER=(str, 'postgres'),
    DB_PASSWORD=(str, ''),
    DB_HOST=(str, 'localhost'),
    DB_PORT=(str, '5432'),

    # Redis
    REDIS_URL=(str, 'redis://localhost:6379/0'),
    REDIS_HOST=(str, 'localhost'),
    REDIS_PORT=(int, 6379),
    REDIS_DB=(int, 0),

    # Email
    EMAIL_BACKEND=(str, 'django.core.mail.backends.console.EmailBackend'),
    SENDGRID_API_KEY=(str, ''),
    DEFAULT_FROM_EMAIL=(str, 'noreply@example.com'),
    SERVER_EMAIL=(str, 'noreply@example.com'),

    # AWS S3
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_STORAGE_BUCKET_NAME=(str, ''),
    AWS_S3_REGION_NAME=(str, 'us-east-1'),
    AWS_S3_CUSTOM_DOMAIN=(str, ''),
    AWS_DEFAULT_ACL=(str, 'private'),
    AWS_S3_FILE_OVERWRITE=(bool, False),

    # Celery
    CELERY_BROKER_URL=(str, 'redis://localhost:6379/1'),
    CELERY_RESULT_BACKEND=(str, 'redis://localhost:6379/1'),

    # JWT
    JWT_SECRET_KEY=(str, ''),
    JWT_ACCESS_TOKEN_LIFETIME=(int, 3600),
    JWT_REFRESH_TOKEN_LIFETIME=(int, 604800),

    # Rate Limiting
    RATE_LIMIT_ENABLED=(bool, True),
    RATE_LIMIT_PER_MINUTE=(int, 100),
    RATE_LIMIT_PER_HOUR=(int, 1000),

    # Monitoring
    SENTRY_DSN=(str, ''),
    LOG_LEVEL=(str, 'INFO'),
    LOG_FILE=(str, '/var/log/django/headless_backend.log'),

    # Security
    CORS_ALLOWED_ORIGINS=(list, ['http://localhost:3000']),
    CSRF_TRUSTED_ORIGINS=(list, ['http://localhost:3000']),
    SECURE_SSL_REDIRECT=(bool, False),
    SECURE_HSTS_SECONDS=(int, 31536000),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, True),
    SECURE_HSTS_PRELOAD=(bool, True),

    # File Upload
    FILE_UPLOAD_MAX_MEMORY_SIZE=(int, 10485760),  # 10MB
    DATA_UPLOAD_MAX_MEMORY_SIZE=(int, 10485760),  # 10MB

    # Cache
    CACHE_TTL=(int, 300),  # 5 minutes
    CACHE_MAX_ENTRIES=(int, 1000),

    # Health Check
    HEALTH_CHECK_ENABLED=(bool, True),
    HEALTH_CHECK_DATABASE=(bool, True),
    HEALTH_CHECK_CACHE=(bool, True),
    HEALTH_CHECK_STORAGE=(bool, True),
)

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "django_extensions",
    "storages",
    "anymail",
    "django_redis",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",

    # Local apps
    "apps.common",
    "apps.accounts",
    "apps.organizations",
    "apps.users",
    "apps.teams",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Add rate limiting middleware if enabled
if env('RATE_LIMIT_ENABLED'):
    MIDDLEWARE.insert(-1, "django_ratelimit.middleware.RatelimitMiddleware")

ROOT_URLCONF = "headless_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "headless_backend.wsgi.application"

# Database Configuration
DATABASES = {
    "default": env.db()
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': f"{env('RATE_LIMIT_PER_MINUTE')}/min",
        'user': f"{env('RATE_LIMIT_PER_HOUR')}/hour"
    }
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=env('JWT_ACCESS_TOKEN_LIFETIME')),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=env('JWT_REFRESH_TOKEN_LIFETIME')),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env('JWT_SECRET_KEY') or SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')

# Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')
    SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS')
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SECURE_HSTS_INCLUDE_SUBDOMAINS')
    SECURE_HSTS_PRELOAD = env('SECURE_HSTS_PRELOAD')
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'Headless SaaS Platform API',
    'DESCRIPTION': 'Comprehensive multi-tenant SaaS platform with AI capabilities',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'SCHEMA_PATH_PREFIX': '/api/',
}

# Redis Configuration
REDIS_URL = env('REDIS_URL')
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_DB = env('REDIS_DB')

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            }
        },
        'KEY_PREFIX': 'headless_backend',
        'TIMEOUT': env('CACHE_TTL'),
        'MAX_ENTRIES': env('CACHE_MAX_ENTRIES'),
    }
}

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('SERVER_EMAIL')

# SendGrid Configuration
if 'sendgrid' in EMAIL_BACKEND.lower():
    SENDGRID_API_KEY = env('SENDGRID_API_KEY')
    ANYMAIL = {
        'SENDGRID_API_KEY': SENDGRID_API_KEY,
    }

# AWS S3 Configuration
if env('AWS_ACCESS_KEY_ID'):
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL')
    AWS_S3_FILE_OVERWRITE = env('AWS_S3_FILE_OVERWRITE')

    # Use S3 for media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Celery Configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# File Upload Configuration
FILE_UPLOAD_MAX_MEMORY_SIZE = env('FILE_UPLOAD_MAX_MEMORY_SIZE')
DATA_UPLOAD_MAX_MEMORY_SIZE = env('DATA_UPLOAD_MAX_MEMORY_SIZE')
FILE_UPLOAD_PERMISSIONS = 0o644

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': env('LOG_LEVEL'),
            'class': 'logging.FileHandler',
            'filename': env('LOG_FILE'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': env('LOG_LEVEL'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': env('LOG_LEVEL'),
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': env('LOG_LEVEL'),
            'propagate': False,
        },
    },
}

# Sentry Configuration
if env('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=True,
                cache_spans=True,
            ),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment='production' if not DEBUG else 'development',
    )

# Health Check Configuration
if env('HEALTH_CHECK_ENABLED'):
    HEALTH_CHECK = {
        'DISK_USAGE_MAX': 90,  # percent
        'MEMORY_MIN': 100,  # in MB
    }

# Rate Limiting Configuration
RATELIMIT_ENABLE = env('RATE_LIMIT_ENABLED')
RATELIMIT_USE_CACHE = 'default'

# Guardian Configuration
GUARDIAN_MONKEY_PATCH = False
