@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      DEPLOY TO FIREBASE HOSTING (After API Enabled)
echo ════════════════════════════════════════════════════════════════
echo.

echo ⚠️  Make sure you've enabled Cloud Run API first!
echo    If not, run: enable_cloud_run_api.bat
echo.
pause

echo.
echo 📦 Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ❌ Failed to collect static files
    pause
    exit /b 1
)

echo.
echo ✅ Static files collected
echo.

echo 🔥 Deploying to Firebase Hosting...
echo    This may take 1-2 minutes...
echo.
firebase deploy --only hosting

if %errorlevel% equ 0 (
    echo.
    echo ════════════════════════════════════════════════════════════════
    echo      ✅ DEPLOYMENT SUCCESSFUL!
    echo ════════════════════════════════════════════════════════════════
    echo.
    echo 🌐 Your website is now live at:
    echo    https://shiku-beuty-hub.web.app
    echo    https://shiku-beuty-hub.firebaseapp.com
    echo.
    echo 💡 Note: This deploys static files.
    echo    For full Django app, deploy backend to Cloud Run next.
    echo.
) else (
    echo.
    echo ❌ Deployment failed!
    echo.
    echo Possible reasons:
    echo    1. Cloud Run API not enabled yet (wait 2-3 more minutes)
    echo    2. Not logged in to Firebase (run: firebase login)
    echo    3. Project not set (run: firebase use shiku-beuty-hub)
    echo.
)

pause

