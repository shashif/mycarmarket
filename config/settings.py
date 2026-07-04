# ==========================================
# MyCarMarket
# Version: v1.5.7
# File: config/settings.py
# Description: Production Deployment, Security & Logging Settings
# ==========================================

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


# ==========================================
# SECTION 01: SECURITY
# START
# ==========================================

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'change-this-secret-key-before-production'
)

DEBUG = os.environ.get(
    'DJANGO_DEBUG',
    'True'
) == 'True'

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost,0.0.0.0,mycarmarket.com.au,www.mycarmarket.com.au'
).split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://127.0.0.1:8000,http://localhost:8000,https://mycarmarket.com.au,https://www.mycarmarket.com.au'
).split(',')

# ==========================================
# SECTION 01: SECURITY
# END
# ==========================================


# ==========================================
# SECTION 02: APPLICATIONS
# START
# ==========================================

INSTALLED_APPS = [

    'core',
    'vehicles',
    'accounts',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
]

# ==========================================
# SECTION 02: APPLICATIONS
# END
# ==========================================


# ==========================================
# SECTION 03: MIDDLEWARE
# START
# ==========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================================
# SECTION 03: MIDDLEWARE
# END
# ==========================================


# ==========================================
# SECTION 04: URLS / WSGI
# START
# ==========================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ==========================================
# SECTION 04: URLS / WSGI
# END
# ==========================================


# ==========================================
# SECTION 05: TEMPLATES
# START
# ==========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==========================================
# SECTION 05: TEMPLATES
# END
# ==========================================


# ==========================================
# SECTION 06: DATABASE
# START
# ==========================================

DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==========================================
# SECTION 06: DATABASE
# END
# ==========================================


# ==========================================
# SECTION 07: PASSWORD VALIDATION
# START
# ==========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==========================================
# SECTION 07: PASSWORD VALIDATION
# END
# ==========================================


# ==========================================
# SECTION 08: LANGUAGE / TIME
# START
# ==========================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Melbourne'
USE_I18N = True
USE_TZ = True

SITE_ID = 1

# ==========================================
# SECTION 08: LANGUAGE / TIME
# END
# ==========================================


# ==========================================
# SECTION 09: STATIC / MEDIA FILES
# START
# ==========================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================
# SECTION 09: STATIC / MEDIA FILES
# END
# ==========================================


# ==========================================
# SECTION 10: AUTH REDIRECTS
# START
# ==========================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'car_list'
LOGOUT_REDIRECT_URL = 'car_list'

# ==========================================
# SECTION 10: AUTH REDIRECTS
# END
# ==========================================


# ==========================================
# SECTION 11: EMAIL SETTINGS
# START
# ==========================================

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'
)

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    'MyCarMarket Australia <no-reply@mycarmarket.com.au>'
)

CONTACT_EMAIL = os.environ.get(
    'CONTACT_EMAIL',
    'support@mycarmarket.com.au'
)

# ==========================================
# SECTION 11: EMAIL SETTINGS
# END
# ==========================================


# ==========================================
# SECTION 12: SITE URL
# START
# ==========================================

SITE_URL = os.environ.get(
    'SITE_URL',
    'http://127.0.0.1:8000'
)

# ==========================================
# SECTION 12: SITE URL
# END
# ==========================================


# ==========================================
# SECTION 13: GOOGLE SERVICES
# START
# ==========================================

GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')
GOOGLE_ADSENSE_ID = os.environ.get('GOOGLE_ADSENSE_ID', '')
GOOGLE_SITE_VERIFICATION = os.environ.get('GOOGLE_SITE_VERIFICATION', '')

# ==========================================
# SECTION 13: GOOGLE SERVICES
# END
# ==========================================


# ==========================================
# SECTION 14: GOOGLE RECAPTCHA
# START
# ==========================================

RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY', '')

# ==========================================
# SECTION 14: GOOGLE RECAPTCHA
# END
# ==========================================


# ==========================================
# SECTION 15: PRODUCTION SECURITY SETTINGS
# START
# ==========================================

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
REFERRER_POLICY = 'strict-origin-when-cross-origin'

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = False

    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ==========================================
# SECTION 15: PRODUCTION SECURITY SETTINGS
# END
# ==========================================


# ==========================================
# SECTION 16: LOGGING
# START
# ==========================================

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ==========================================
# SECTION 16: LOGGING
# END
# ==========================================


# ==========================================
# SECTION 17: DEFAULT AUTO FIELD
# START
# ==========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# SECTION 17: DEFAULT AUTO FIELD
# END
# ==========================================

# ==========================================
# SECTION 18: FILE UPLOAD LIMITS
# START
# ==========================================

# Maximum request size (25 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024

# Files larger than 5 MB are streamed to disk
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# Maximum number of uploaded form fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# ==========================================
# SECTION 18: FILE UPLOAD LIMITS
# END
# ==========================================