import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRUE_VALUES = [True, "True", "true", "1"]

# Django settings
SECRET_KEY = os.getenv("SECRET_KEY")

# Debug Logging
DEBUG = os.getenv("DEBUG", False) in TRUE_VALUES
LOG_QUERIES = False
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

# localhost and 127.0.0.1 are allowed because the deployment process checks the health endpoint with a
# request to localhost:port
DEFAULT_ALLOWED_HOSTS = "localhost,127.0.0.1,.forzamor.nl"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")

INTERNAL_IPS = ("127.0.0.1", "0.0.0.0")

SITE_ID = 1
SITE_NAME = os.getenv("SITE_NAME", "DefaultName API")
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "localhost")

ORGANIZATION_NAME = os.getenv("ORGANIZATION_NAME")

# Accept incidents within this geographic bounding box in
# format: <lon_min>,<lat_min>,<lon_max>,<lat_max> (WGS84)
# default value covers The Netherlands
BOUNDING_BOX = [
    float(i) for i in os.getenv("BOUNDING_BOX", "3.3,50.7,7.3,53.6").split(",")
]


# Django security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "strict-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = False
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_NAME = "__Secure-sessionid" if not DEBUG else "sessionid"
CSRF_COOKIE_NAME = "__Secure-csrftoken" if not DEBUG else "csrftoken"
SESSION_COOKIE_SAMESITE = "Strict" if not DEBUG else "Lax"
CSRF_COOKIE_SAMESITE = "Strict" if not DEBUG else "Lax"

# Settings for Content-Security-Policy header
CSP_DEFAULT = ("'self'",)
CSP_DEFAULT_SRC = CSP_DEFAULT
CSP_FRAME_ANCESTORS = CSP_DEFAULT
CSP_SCRIPT_SRC = CSP_DEFAULT
CSP_IMG_SRC = CSP_DEFAULT
CSP_STYLE_SRC = CSP_DEFAULT
CSP_CONNECT_SRC = CSP_DEFAULT

# Application definition
PROJECT_APPS = [
    "apps.health",
    "apps.users",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.gis",
    # Third party
    "corsheaders",
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework_gis",
    "health_check",
    "health_check.cache",
    "health_check.storage",
    "health_check.db",
    "health_check.contrib.migrations",
] + PROJECT_APPS

MIDDLEWARE = [
    "profilr_api_services.middleware.ApiServiceExceptionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# django-permissions-policy settings
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# Database settings
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST_OVERRIDE")
DATABASE_PORT = os.getenv("DATABASE_PORT_OVERRIDE")

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DATABASE_NAME,  # noqa:
        "USER": DATABASE_USER,  # noqa
        "PASSWORD": DATABASE_PASSWORD,  # noqa
        "HOST": DATABASE_HOST,  # noqa
        "PORT": DATABASE_PORT,  # noqa
    },
}  # noqa

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOCAL_DEVELOPMENT_AUTHENTICATION = (
    os.getenv("LOCAL_DEVELOPMENT_AUTHENTICATION", True) in TRUE_VALUES
)

# Internationalization
LANGUAGE_CODE = "nl-NL"
TIME_ZONE = "Europe/Amsterdam"
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATETIME_FORMAT = "l d-m-Y, H:i"  # e.g. "Donderdag 06-09-2018, 13:56"

# Static files (CSS, JavaScript, Images) and media files
STATIC_URL = "/api/static/"
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "static")
MEDIA_URL = "/api/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "media")

# Django REST framework settings
REST_FRAMEWORK = dict(
    PAGE_SIZE=100,
    UNAUTHENTICATED_USER={},
    UNAUTHENTICATED_TOKEN={},
    DEFAULT_AUTHENTICATION_CLASSES=["apps.auth.backend.AuthBackend"],
    DEFAULT_PAGINATION_CLASS="rest_framework.pagination.LimitOffsetPagination",
    DEFAULT_FILTER_BACKENDS=("django_filters.rest_framework.DjangoFilterBackend",),
    DEFAULT_THROTTLE_RATES={
        "nouser": os.getenv("PUBLIC_THROTTLE_RATE", "60/hour"),
    },
    # DEFAULT_RENDERER_CLASSES=(
    #     "rest_framework.renderers.JSONRenderer",
    #     "rest_framework.renderers.BrowsableAPIRenderer",
    # ),
)

MSB_API_URL = os.getenv("MSB_API_URL")
INCIDENT_API_URL = os.getenv("INCIDENT_API_URL", f"{MSB_API_URL}/sbmob/api")
INCIDENT_API_HEALTH_CHECK_URL = os.getenv(
    "INCIDENT_API_HEALTH_CHECK_URL", f"{MSB_API_URL}/sbmob/api/logout"
)
INCIDENT_API_SERVICE = os.getenv(
    "INCIDENT_API_SERVICE", "profilr_api_services.IncidentAPIService"
)

# The URL of the Frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", None)

# Default pdok settings
PDOK_API_URL = os.getenv("PDOK_API_URL", "https://geodata.nationaalgeoregister.nl")

# Default pdok municipalities
DEFAULT_PDOK_MUNICIPALITIES = os.getenv("DEFAULT_PDOK_MUNICIPALITIES", "").split(",")

GEMEENTE_CODE = "GM0599"

REDIS_URL = "redis://redis:6379"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
