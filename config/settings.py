# ==========================================
# MyCarMarket
# Version: v1.1.0
# File: config/settings.py
# Email Notification System + Stripe Checkout Setup
# ==========================================

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SECURITY
# ==========================================

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'change-this-secret-key-before-production'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost'
).split(',')


# ==========================================
# APPLICATIONS
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
]


# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================
# URLS / WSGI
# ==========================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# ==========================================
# TEMPLATES
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
# DATABASE
# ==========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# PASSWORD VALIDATION
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
# LANGUAGE / TIME
# ==========================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Melbourne'
USE_I18N = True
USE_TZ = True

SITE_ID = 1


# ==========================================
# STATIC / MEDIA FILES
# ==========================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# AUTH REDIRECTS
# ==========================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'car_list'
LOGOUT_REDIRECT_URL = 'car_list'


# ==========================================
# EMAIL SETTINGS
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
# STRIPE PAYMENT SETTINGS
# v1.1.0 Stripe Checkout Setup
# ==========================================

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')

STRIPE_PRICE_STARTER = os.environ.get('STRIPE_PRICE_STARTER', '')
STRIPE_PRICE_PROFESSIONAL = os.environ.get('STRIPE_PRICE_PROFESSIONAL', '')
STRIPE_PRICE_PREMIUM = os.environ.get('STRIPE_PRICE_PREMIUM', '')
STRIPE_PRICE_ENTERPRISE = os.environ.get('STRIPE_PRICE_ENTERPRISE', '')

SITE_URL = os.environ.get(
    'SITE_URL',
    'http://127.0.0.1:8000'
)

STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# ==========================================
# PRODUCTION SECURITY SETTINGS
# Only active when DEBUG=False
# ==========================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = 'DENY'

    CSRF_TRUSTED_ORIGINS = os.environ.get(
        'CSRF_TRUSTED_ORIGINS',
        ''
    ).split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []


# ==========================================
# END SETTINGS
# ==========================================