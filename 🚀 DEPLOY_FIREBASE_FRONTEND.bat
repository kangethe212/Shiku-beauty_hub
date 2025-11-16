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
echo [OK] Static files collected!

echo.
echo [2/3] Checking Firebase project...
firebase use shiku-beuty-hub
if %errorlevel% neq 0 (
    echo [ERROR] Failed to set Firebase project
    pause
    exit /b 1
)
echo [OK] Firebase project set!

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
echo   ✅ DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your static files are live at:
echo   🌐 https://shiku-beuty-hub.web.app
echo   🌐 https://shiku-beuty-hub.firebaseapp.com
echo.
echo ⚠️  NOTE: This deploys static files only (CSS, JS, images)
echo    For full Django app, deploy backend to Railway
echo.
pause

