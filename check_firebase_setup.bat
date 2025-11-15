@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      FIREBASE DEPLOYMENT - SETUP VERIFICATION
echo ════════════════════════════════════════════════════════════════
echo.

set errors=0

echo Checking prerequisites...
echo.

REM Check Google Cloud SDK
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK: NOT INSTALLED
    echo    Install from: https://cloud.google.com/sdk/docs/install
    set /a errors+=1
) else (
    echo ✅ Google Cloud SDK: INSTALLED
    gcloud --version | findstr /C:"Google Cloud SDK"
)

echo.

REM Check Firebase CLI
where firebase >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI: NOT INSTALLED
    echo    Install with: npm install -g firebase-tools
    set /a errors+=1
) else (
    echo ✅ Firebase CLI: INSTALLED
    firebase --version
)

echo.

REM Check Docker
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker: NOT INSTALLED
    echo    Install from: https://www.docker.com/products/docker-desktop
    set /a errors+=1
) else (
    echo ✅ Docker: INSTALLED
    docker --version
)

echo.

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python: NOT INSTALLED
    set /a errors+=1
) else (
    echo ✅ Python: INSTALLED
    python --version
)

echo.

REM Check if logged into gcloud
gcloud auth list 2>nul | findstr /C:"ACTIVE" >nul
if %errorlevel% neq 0 (
    echo ⚠️  Google Cloud: NOT LOGGED IN
    echo    Run: gcloud auth login
    set /a errors+=1
) else (
    echo ✅ Google Cloud: LOGGED IN
    gcloud auth list | findstr "ACTIVE"
)

echo.

REM Check if logged into Firebase
firebase projects:list >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Firebase: NOT LOGGED IN
    echo    Run: firebase login
    set /a errors+=1
) else (
    echo ✅ Firebase: LOGGED IN
)

echo.

REM Check if firebase.json exists
if exist firebase.json (
    echo ✅ firebase.json: EXISTS
) else (
    echo ❌ firebase.json: NOT FOUND
    echo    Run: firebase init hosting
    set /a errors+=1
)

echo.

REM Check if Dockerfile exists
if exist Dockerfile (
    echo ✅ Dockerfile: EXISTS
) else (
    echo ❌ Dockerfile: NOT FOUND
    set /a errors+=1
)

echo.

REM Check if requirements.txt exists
if exist requirements.txt (
    echo ✅ requirements.txt: EXISTS
) else (
    echo ❌ requirements.txt: NOT FOUND
    set /a errors+=1
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.

if %errors% equ 0 (
    echo ✅ ALL CHECKS PASSED! You're ready to deploy!
    echo.
    echo Next steps:
    echo 1. Read: 🔥 FIREBASE_STEP_BY_STEP.md
    echo 2. Run: deploy_firebase_simple.bat
) else (
    echo ❌ FOUND %errors% ISSUE(S) - Please fix them before deploying
    echo.
    echo See: 🔥 FIREBASE_STEP_BY_STEP.md for detailed instructions
)

echo.
pause

