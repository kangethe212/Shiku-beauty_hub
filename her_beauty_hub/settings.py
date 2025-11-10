"""
Django settings for Shiku Beauty Hub project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-change-this-in-production-xyz123abc456def789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Beautiful modern admin interface (MUST BE BEFORE django.contrib.admin)
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

# PostgreSQL (Production - ACTIVE NOW!)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shiku_db',                  # Your database name
        'USER': 'postgres',                  # Your PostgreSQL username
        'PASSWORD': '7457@Benson',           # Your PostgreSQL password
        'HOST': 'localhost',                 # Database host (localhost for local)
        'PORT': '5432',                      # PostgreSQL default port
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

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration (for contact form notifications)
# Using Gmail SMTP for instant email notifications
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bennymaish01@gmail.com'
EMAIL_HOST_PASSWORD = ''  # ⚠️ ADD YOUR GMAIL APP PASSWORD HERE (see GMAIL_SETUP.md)
DEFAULT_FROM_EMAIL = 'Shiku Beauty Hub <bennymaish01@gmail.com>'

# For development/testing, use console:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Admin email for notifications
ADMIN_EMAIL = 'bennymaish01@gmail.com'

# ============================================================
# INSTANT NOTIFICATION SETTINGS
# ============================================================

# Owner's contact details
OWNER_PHONE = '254796465104'  # WhatsApp number (international format)
OWNER_EMAIL = 'bennymaish01@gmail.com'  # Owner's email for notifications

# Telegram Bot (RECOMMENDED - Free & Instant!)
# Setup: Chat with @BotFather on Telegram to create bot
TELEGRAM_BOT_TOKEN = ''  # Get from @BotFather
TELEGRAM_CHAT_ID = ''    # Get from bot after first message

# WhatsApp Business API (Optional - Requires paid service)
# Option 1: Twilio (https://twilio.com/)
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'

# Option 2: Africa's Talking (Popular in Kenya)
AFRICASTALKING_USERNAME = ''  # Your username
AFRICASTALKING_API_KEY = ''   # Your API key

# Discord Webhook (Optional - Free!)
DISCORD_WEBHOOK_URL = ''  # Create webhook in Discord server

# Date input format for booking
DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']


# ============================================================
# JAZZMIN ADMIN THEME CONFIGURATION
# ============================================================

JAZZMIN_SETTINGS = {
    # Title & Logo
    "site_title": "Shiku Beauty Hub",
    "site_header": "Shiku Beauty Hub 💎",
    "site_brand": "Shiku Beauty Hub",
    "site_logo": "logo-icon.svg",  # Use our custom logo
    "login_logo": "logo.svg",
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": "favicon.svg",
    
    # Welcome Message
    "welcome_sign": "Welcome to Shiku Beauty Hub Control Center",
    
    # Copyright
    "copyright": "Shiku Beauty Hub © 2025",
    
    # Search in sidebar
    "search_model": ["auth.User", "beautyhub.HairStyle", "beautyhub.Perfume", "beautyhub.ClothingItem", "beautyhub.OrderMessage"],
    
    # User Menu
    "user_avatar": None,
    
    # Top Menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Website", "url": "/", "new_window": True},
        {"model": "beautyhub.OrderMessage"},
        {"app": "beautyhub"},
    ],
    
    # User menu on the right side
    "usermenu_links": [
        {"name": "View Website", "url": "/", "icon": "fas fa-globe", "new_window": True},
        {"model": "auth.user"},
    ],
    
    # Side Menu Items
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Custom Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "beautyhub.HairStyle": "fas fa-cut",
        "beautyhub.Perfume": "fas fa-spray-can",
        "beautyhub.ClothingItem": "fas fa-tshirt",
        "beautyhub.OrderMessage": "fas fa-shopping-cart",
        "beautyhub.Booking": "fas fa-calendar-check",
        "beautyhub.Video": "fas fa-video",
        "beautyhub.GalleryItem": "fas fa-images",
        "beautyhub.DailyOffer": "fas fa-fire",
        "beautyhub.ContactMessage": "fas fa-envelope",
        "beautyhub.Service": "fas fa-concierge-bell",
        "beautyhub.Product": "fas fa-box",
    },
    
    # Default icon for models
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related modal
    "related_modal_active": True,
    
    # Custom CSS
    "custom_css": None,
    "custom_js": None,
    
    # Show language chooser
    "show_ui_builder": False,
    
    # Change user form button
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
    
    # Override settings per language
    "language_chooser": False,
}

# Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-pink",
    "accent": "accent-pink",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-pink",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True,
}

# Custom CSS for Jazzmin (Shiku Beauty Hub colors)
JAZZMIN_SETTINGS["custom_css"] = "admin/custom_admin.css"

