# 📝 .env File Guide

## ✅ What's Been Set Up

Your project now supports `.env` files for environment variables! Here's what changed:

1. **Updated `settings.py`** - Now uses `python-decouple` to automatically load from `.env` file
2. **Created helper script** - `create_env_file.bat` to generate your `.env` file
3. **`.env` is in `.gitignore`** - Your secrets won't be committed to git

---

## 🚀 Quick Start

### Option 1: Use the Helper Script (Recommended)

```bash
create_env_file.bat
```

This will:
- Generate a secure secret key automatically
- Create a `.env` file with all the necessary variables
- Set up default values

### Option 2: Create Manually

1. Create a file named `.env` in your project root (`C:\shiku salon\.env`)
2. Copy the template below and fill in your values

---

## 📋 .env File Template

```env
# Django Settings
# This file contains your local environment variables
# DO NOT commit this file to git (it's in .gitignore)

# Secret Key - Generate a new one for production!
# Run: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-secret-key-here

# Debug Mode (True for development, False for production)
DEBUG=True

# Site URL (for notifications and links)
SITE_URL=http://localhost:3000

# Database Configuration
# For local development with SQLite (default):
# Leave DATABASE_URL empty or unset

# For PostgreSQL (Railway/Cloud SQL):
# DATABASE_URL=postgresql://user:password@host:port/database
DATABASE_URL=

# Email Configuration
EMAIL_PASSWORD=your-email-password-here

# Telegram Bot (Optional - for notifications)
# Get token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Twilio (Optional - for WhatsApp notifications)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Africa's Talking (Optional - popular in Kenya)
AFRICASTALKING_USERNAME=
AFRICASTALKING_API_KEY=

# Discord Webhook (Optional - for notifications)
DISCORD_WEBHOOK_URL=
```

---

## 🔑 How It Works

### Before (using os.environ):
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-value')
```
- Only reads from system environment variables
- Doesn't read from `.env` file

### After (using python-decouple):
```python
from decouple import config
SECRET_KEY = config('SECRET_KEY', default='default-value')
```
- ✅ Reads from `.env` file automatically
- ✅ Falls back to system environment variables
- ✅ Uses default value if neither exists

---

## 📝 Environment Variables Explained

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (auto-generated) | `django-insecure-abc123...` |
| `DEBUG` | Debug mode | `True` or `False` |
| `SITE_URL` | Your website URL | `http://localhost:3000` |

### Optional Variables

| Variable | Description | When to Use |
|----------|-------------|-------------|
| `DATABASE_URL` | PostgreSQL connection string | When using PostgreSQL (Railway/Cloud SQL) |
| `EMAIL_PASSWORD` | Gmail app password | When sending emails |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | For Telegram notifications |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | For Telegram notifications |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | For WhatsApp notifications |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | For WhatsApp notifications |
| `AFRICASTALKING_USERNAME` | Africa's Talking username | For SMS/WhatsApp in Kenya |
| `AFRICASTALKING_API_KEY` | Africa's Talking API key | For SMS/WhatsApp in Kenya |
| `DISCORD_WEBHOOK_URL` | Discord webhook URL | For Discord notifications |

---

## 🔒 Security Notes

1. **Never commit `.env` to git** - It's already in `.gitignore`
2. **Generate a new SECRET_KEY for production** - Don't use the default!
3. **Set DEBUG=False in production** - Always!
4. **Keep your `.env` file secure** - Don't share it

---

## 🚀 For Firebase Deployment

When deploying to Firebase/Cloud Run, you'll set environment variables in Cloud Run, not in `.env` file:

```bash
gcloud run services update shiku-beuty-hub \
  --update-env-vars "SECRET_KEY=your-key,DEBUG=False"
```

The `.env` file is for **local development only**.

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'decouple'"
**Solution:** Install python-decouple
```bash
pip install python-decouple
```

### Variables not loading from .env
**Solution:** 
1. Make sure `.env` file is in the project root (same folder as `manage.py`)
2. Check for typos in variable names
3. Restart your Django server

### .env file not found
**Solution:** 
- Run `create_env_file.bat` to create it
- Or create it manually in the project root

---

## ✅ Checklist

- [ ] `.env` file created
- [ ] `SECRET_KEY` generated (use the helper script!)
- [ ] `DEBUG` set to `True` for development
- [ ] `SITE_URL` set correctly
- [ ] `DATABASE_URL` set if using PostgreSQL
- [ ] Optional variables added if needed
- [ ] `.env` file is NOT committed to git (check `.gitignore`)

---

**🎉 You're all set! Your Django app will now automatically load variables from `.env` file!**

