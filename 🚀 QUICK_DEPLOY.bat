@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      🚀 COMPLETE FIREBASE + CLOUD RUN DEPLOYMENT
echo ════════════════════════════════════════════════════════════════
echo.

echo 📋 DEPLOYMENT CHECKLIST:
echo.
echo This will guide you through deploying your full Django app.
echo.
echo ✅ Step 1: Enable Cloud Run API (Browser should open)
echo ✅ Step 2: Install Google Cloud SDK (if needed)
echo ✅ Step 3: Set up Cloud SQL Database
echo ✅ Step 4: Deploy Django to Cloud Run
echo ✅ Step 5: Connect Firebase to Cloud Run
echo ✅ Step 6: Run Migrations
echo ✅ Step 7: Create Admin User
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════
echo      STEP 1: ENABLE CLOUD RUN API
echo ════════════════════════════════════════════════════════════════
echo.
echo Opening Cloud Run API page in browser...
start https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=140804076783
echo.
echo 📝 INSTRUCTIONS:
echo    1. Click "ENABLE" button
echo    2. Wait 2-3 minutes for activation
echo    3. Come back here and press any key to continue...
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════
echo      STEP 2: CHECK PREREQUISITES
echo ════════════════════════════════════════════════════════════════
echo.

REM Check Google Cloud SDK
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK not installed
    echo.
    echo Please install from: https://cloud.google.com/sdk/docs/install
    echo.
    echo After installing, restart this script.
    pause
    exit /b 1
) else (
    echo ✅ Google Cloud SDK installed
    gcloud --version | findstr /C:"Google Cloud SDK"
)

echo.

REM Check Docker
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not installed
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    echo After installing, restart this script.
    pause
    exit /b 1
) else (
    echo ✅ Docker installed
    docker --version
)

echo.
echo ✅ All prerequisites met!
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════
echo      NEXT STEPS
echo ════════════════════════════════════════════════════════════════
echo.
echo Choose how to proceed:
echo.
echo 1. Use interactive deployment script (Recommended)
echo 2. Follow manual guide
echo 3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    call deploy_to_cloud_run.bat
) else if "%choice%"=="2" (
    echo.
    echo 📖 Opening deployment guide...
    start 🚀 COMPLETE_DEPLOYMENT_GUIDE.md
    echo.
    echo See the guide for detailed step-by-step instructions.
) else (
    exit /b 0
)

pause

