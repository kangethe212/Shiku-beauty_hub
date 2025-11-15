"""
Django settings for Shiku Beauty Hub project.
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# Loads from .env file or environment variable
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-xyz123abc456def789')

# SECURITY WARNING: don't run with debug turned on in production!
# Loads from .env file or environment variable
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    '.railway.app',  # Allow all Railway subdomains
    'yamanote.proxy.rlwy.net',
    '.web.app',  # Firebase Hosting default domain
    '.firebaseapp.com',  # Firebase Hosting default domain
    '*.run.app',  # Google Cloud Run domains
    '*'  # Allow all hosts (for Railway and Firebase auto-generated domains)
]

# CSRF trusted origins for Firebase Hosting and Cloud Run
CSRF_TRUSTED_ORIGINS = [
    'https://*.web.app',
    'https://*.firebaseapp.com',
    'https://shiku-beuty-hub.web.app',  # Your Firebase domain
    'https://shiku-beuty-hub.firebaseapp.com',  # Your Firebase domain
    'https://*.run.app',
    'https://*.railway.app',
]


# Application definition

INSTALLED_APPS = [
    # 'jazzmin',  # Temporarily disabled for Railway deployment
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'beautyhub',  # Our main app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files for production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'her_beauty_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'her_beauty_hub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# ============================================================
# DATABASE CONFIGURATION
# ============================================================

# SQLite (Backup - Deactivated)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database configuration with Railway support
import dj_database_url

# Check if running on Railway (it sets DATABASE_URL env variable)
# Also check .env file for DATABASE_URL
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Use DATABASE_URL with SSL and optimized settings
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=60,  # Reduced from 600 to prevent stale connections
            conn_health_checks=True,
            ssl_require=True,
        )
    }
    # Add SSL and connection options for Railway PostgreSQL
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
        'connect_timeout': 10,
        'options': '-c statement_timeout=30000'  # 30 second timeout
    }
    DATABASES['default']['CONN_MAX_AGE'] = 60
else:
    # Use Railway database directly (fallback)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'railway',
            'USER': 'postgres',
            'PASSWORD': 'UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ',
            'HOST': 'yamanote.proxy.rlwy.net',
            'PORT': '27057',
            'CONN_MAX_AGE': 60,
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 10,
                'options': '-c statement_timeout=30000'
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise configuration for Railway
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration (for contact form notifications)
# Using console backend for Railway (no SMTP password needed)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bennymaish01@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD', default='')  # Safe fallback
DEFAULT_FROM_EMAIL = 'Shiku Beauty Hub <bennymaish01@gmail.com>'

# Admin email for notifications
ADMIN_EMAIL = 'bennymaish01@gmail.com'

# Site URL for notifications
SITE_URL = config('SITE_URL', default='http://localhost:3000')

# ============================================================
# INSTANT NOTIFICATION SETTINGS
# ============================================================

# Owner's contact details
OWNER_PHONE = '254796465104'  # WhatsApp number (international format)
OWNER_EMAIL = 'bennymaish01@gmail.com'  # Owner's email for notifications

# Telegram Bot (RECOMMENDED - Free & Instant!)
# Setup: Chat with @BotFather on Telegram to create bot
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')

# WhatsApp Business API (Optional - Requires paid service)
# Option 1: Twilio (https://twilio.com/)
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'

# Option 2: Africa's Talking (Popular in Kenya)
AFRICASTALKING_USERNAME = config('AFRICASTALKING_USERNAME', default='')
AFRICASTALKING_API_KEY = config('AFRICASTALKING_API_KEY', default='')

# Discord Webhook (Optional - Free!)
DISCORD_WEBHOOK_URL = config('DISCORD_WEBHOOK_URL', default='')

# Date input format for booking
DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']


# ============================================================
# JAZZMIN ADMIN THEME CONFIGURATION (Temporarily Disabled for Railway)
# ============================================================
# Note: Jazzmin is disabled to fix Railway deployment
# Standard Django admin will work perfectly
# You can re-enable Jazzmin later once deployment is stable

# JAZZMIN_SETTINGS = {
#     # Title & Logo
#     "site_title": "Shiku Beauty Hub",
#     "site_header": "Shiku Beauty Hub 💎",
#     "site_brand": "Shiku Beauty Hub",
#     "site_logo": "logo-icon.svg",
#     "login_logo": "logo.svg",
#     "login_logo_dark": None,
#     "site_logo_classes": "img-circle",
#     "site_icon": "favicon.svg",
#     # ... (all other settings)
# }

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     # ... (all other settings)
# }

