import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

from apps import users
from core.jazzmin_conf import JAZZMIN_SETTINGS  # noqa

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "apps.common",
    "apps.users",
    "apps.item",
    "apps.reaction"
]

EXTERNAL_APPS = [
    "jazzmin",
    'rosetta',
    'modeltranslation',
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    "drf_yasg",
    "django_recaptcha",
    "django_filters",
    'corsheaders',
]

INSTALLED_APPS = EXTERNAL_APPS + DJANGO_APPS + LOCAL_APPS

# Internationalization

TIME_ZONE = "Asia/Tashkent"

USE_TZ = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # "apps.common.middleware.UserLanguageMiddleware"
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware'
]

CORS_ALLOW_ALL_ORIGINS = True

# Internationalization settings
LANGUAGE_CODE = 'uz'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
    ('en', 'English'),
]

# Language cookie (optional, for persistence)
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 365 * 24 * 60 * 60  # 1 year
LANGUAGE_COOKIE_HTTPONLY = True
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# Locale paths for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.users.services.custom_auth.CustomJWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    "PAGE_SIZE": 10,

}

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"
# ASGI_APPLICATION = 'core.asgi.application'

BASE_URL = os.getenv("BASE_URL")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'apps.users.services.custom_model_back.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (BASE_DIR / "static",)

# Media (user uploaded files)
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CACHES
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "KEY_PREFIX": os.getenv("PROJECT_NAME", "project_name"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
    }
}

# CELERY CONFIGURATION
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}")
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}"
)

CELERY_TIMEZONE = "Asia/Tashkent"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# CYPHER CONFIGURATION
# AES
AES_KEY = os.getenv("AES_KEY", "")

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
        }
    }
}

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "webmaster@localhost")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://frontend:5173",
]