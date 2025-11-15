@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      CREATE .ENV FILE FOR SHIKU BEAUTY HUB
echo ════════════════════════════════════════════════════════════════
echo.

if exist .env (
    echo ⚠️  .env file already exists!
    echo.
    set /p overwrite="Do you want to overwrite it? (y/n): "
    if /i not "%overwrite%"=="y" (
        echo Cancelled.
        pause
        exit /b 0
    )
)

echo.
echo Generating secret key...
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > temp_secret.txt
set /p SECRET_KEY=<temp_secret.txt
del temp_secret.txt

echo.
echo Creating .env file...
(
echo # Django Settings
echo # This file contains your local environment variables
echo # DO NOT commit this file to git ^(it's in .gitignore^)
echo.
echo # Secret Key - Generated automatically
echo SECRET_KEY=%SECRET_KEY%
echo.
echo # Debug Mode ^(True for development, False for production^)
echo DEBUG=True
echo.
echo # Site URL ^(for notifications and links^)
echo SITE_URL=http://localhost:3000
echo.
echo # Database Configuration
echo # For local development with SQLite ^(default^):
echo # Leave DATABASE_URL empty or unset
echo.
echo # For PostgreSQL ^(Railway/Cloud SQL^):
echo # DATABASE_URL=postgresql://user:password@host:port/database
echo DATABASE_URL=
echo.
echo # Email Configuration
echo EMAIL_PASSWORD=
echo.
echo # Telegram Bot ^(Optional - for notifications^)
echo # Get token from @BotFather on Telegram
echo TELEGRAM_BOT_TOKEN=
echo TELEGRAM_CHAT_ID=
echo.
echo # Twilio ^(Optional - for WhatsApp notifications^)
echo TWILIO_ACCOUNT_SID=
echo TWILIO_AUTH_TOKEN=
echo TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
echo.
echo # Africa's Talking ^(Optional - popular in Kenya^)
echo AFRICASTALKING_USERNAME=
echo AFRICASTALKING_API_KEY=
echo.
echo # Discord Webhook ^(Optional - for notifications^)
echo DISCORD_WEBHOOK_URL=
) > .env

echo.
echo ✅ .env file created successfully!
echo.
echo 📝 Next steps:
echo    1. Edit .env file to add your configuration values
echo    2. For production, set DEBUG=False
echo    3. Add your DATABASE_URL if using PostgreSQL
echo    4. Add notification tokens if needed
echo.
echo 💡 Tip: The secret key has been generated automatically!
echo.
pause

