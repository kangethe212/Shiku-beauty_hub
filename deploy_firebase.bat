@echo off
echo ============================================================
echo   DEPLOYING FRONTEND TO FIREBASE HOSTING
echo ============================================================
echo.

echo [1/3] Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo [ERROR] Failed to collect static files
    pause
    exit /b 1
)

echo.
echo [2/3] Checking Firebase login...
firebase login --no-localhost
if %errorlevel% neq 0 (
    echo [ERROR] Firebase login failed
    pause
    exit /b 1
)

echo.
echo [3/3] Deploying to Firebase Hosting...
firebase deploy --only hosting
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your site is live at:
echo   https://shiku-beuty-hub.web.app
echo   https://shiku-beuty-hub.firebaseapp.com
echo.
pause

