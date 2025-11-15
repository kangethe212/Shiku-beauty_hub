@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      FIREBASE HOSTING SETUP & DEPLOYMENT
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if Firebase CLI is installed
where firebase >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found!
    echo    Please install: npm install -g firebase-tools
    pause
    exit /b 1
)

echo ✅ Firebase CLI found
echo.

REM Check if logged in
firebase login:list >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Not logged in to Firebase
    echo    Logging in...
    firebase login
) else (
    echo ✅ Logged in to Firebase
)

echo.

REM Set Firebase project
echo 📋 Setting Firebase project to: shiku-beuty-hub
firebase use shiku-beuty-hub
if %errorlevel% neq 0 (
    echo ❌ Failed to set Firebase project
    pause
    exit /b 1
)

echo.

REM Check if .firebaserc exists
if not exist .firebaserc (
    echo 📝 Initializing Firebase project...
    echo    This will create .firebaserc file
    echo.
    echo    When prompted:
    echo    - Select: Use an existing project
    echo    - Choose: shiku-beuty-hub
    echo    - Public directory: staticfiles
    echo    - Single-page app: No
    echo    - Overwrite index.html: No
    echo.
    pause
    echo Y | firebase init hosting --project shiku-beuty-hub
) else (
    echo ✅ Firebase project already initialized
)

echo.

REM Collect static files
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

REM Deploy to Firebase Hosting
echo 🔥 Deploying to Firebase Hosting...
echo.
firebase deploy --only hosting
if %errorlevel% neq 0 (
    echo ❌ Deployment failed!
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════
echo      ✅ DEPLOYMENT COMPLETE!
echo ════════════════════════════════════════════════════════════════
echo.
echo 🌐 Your website should be live at:
echo    https://shiku-beuty-hub.web.app
echo    https://shiku-beuty-hub.firebaseapp.com
echo.
echo 💡 Note: This deploys static files only.
echo    For full Django app, you need Cloud Run backend.
echo.
pause

