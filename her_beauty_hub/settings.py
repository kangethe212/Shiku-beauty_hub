"""
Django settings for Shiku Beauty Hub project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

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
    'shiku-beautyhub-production.up.railway.app',  # Your specific Railway domain
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
    'https://shiku-beautyhub-production.up.railway.app',  # Your specific Railway domain
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Beautiful admin interface
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
# dj_database_url already imported at top

# Railway sets DATABASE_URL automatically when PostgreSQL is added
# Also check for PGDATABASE, PGHOST, etc. (Railway sometimes uses these)
DATABASE_URL = (
    os.environ.get('DATABASE_URL') or
    os.environ.get('PGDATABASE') or
    os.environ.get('POSTGRES_URL')
)

# Try to use PostgreSQL if DATABASE_URL is set
if DATABASE_URL:
    try:
        # Use PostgreSQL from Railway or environment variable
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                ssl_require=True
            )
        }
        # Ensure we're using PostgreSQL
        if 'postgres' not in DATABASES['default'].get('ENGINE', '').lower():
            # If not PostgreSQL, fall back to SQLite
            raise ValueError("Not a PostgreSQL database")
    except Exception:
        # If PostgreSQL config fails, use SQLite fallback
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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
# Use CompressedStaticFilesStorage to avoid manifest file issues
# This provides compression without strict manifest checking for missing .map files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# WhiteNoise settings for better static file serving
WHITENOISE_USE_FINDERS = False  # Don't use finders in production
WHITENOISE_AUTOREFRESH = False  # Don't auto-refresh in production (faster)
WHITENOISE_ROOT = BASE_DIR / 'staticfiles'  # Explicitly set static root for WhiteNoise

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
# ============================================================
# JAZZMIN ADMIN INTERFACE CONFIGURATION
# Beautiful admin panel matching website color theme
# ============================================================

JAZZMIN_SETTINGS = {
    # Site title and branding
    "site_title": "Shiku Beauty Hub",
    "site_header": "Shiku Beauty Hub 💎",
    "site_brand": "Shiku Beauty Hub",
    "site_logo": "logo-icon.svg",
    "login_logo": "logo.svg",
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": "favicon.svg",
    
    # Welcome message
    "welcome_sign": "Welcome to Shiku Beauty Hub Admin",
    "copyright": "Shiku Beauty Hub",
    
    # Theme colors - matching website color scheme
    "theme": "default",  # We'll customize with CSS
    "color_scheme": "light",
    
    # Top menu customization
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    
    # Sidebar customization
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Icons for models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "beautyhub.BusinessInfo": "fas fa-building",
        "beautyhub.Hairstyle": "fas fa-cut",
        "beautyhub.Perfume": "fas fa-spray-can",
        "beautyhub.ClothingItem": "fas fa-tshirt",
        "beautyhub.GalleryItem": "fas fa-images",
        "beautyhub.Testimonial": "fas fa-star",
        "beautyhub.Video": "fas fa-video",
        "beautyhub.Service": "fas fa-spa",
        "beautyhub.Booking": "fas fa-calendar-check",
        "beautyhub.ContactMessage": "fas fa-envelope",
        "beautyhub.OrderMessage": "fas fa-shopping-cart",
    },
    
    # Custom CSS for color theme
    "custom_css": "admin/custom_admin.css",
    "custom_js": None,
    
    # UI tweaks
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    
    # Change view settings
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    
    # Related modal
    "related_modal_active": True,
    
    # Custom links
    "custom_links": {
        "beautyhub": [{
            "name": "View Website",
            "url": "/",
            "icon": "fas fa-external-link-alt",
            "new_window": True,
        }]
    },
}

# Jazzmin UI Tweaks - Custom styling
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-pink",  # Custom color
    "accent": "accent-pink",  # Custom accent
    "navbar": "navbar-pink navbar-dark",  # Pink navbar
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-pink",  # Custom sidebar
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

