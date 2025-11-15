@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      GOOGLE CLOUD SDK - POST-INSTALLATION SETUP
echo ════════════════════════════════════════════════════════════════
echo.

echo ✅ Google Cloud SDK is installed and configured!
echo.
echo 📋 Next steps to complete setup:
echo.

echo ════════════════════════════════════════════════════════════════
echo      STEP 1: VERIFY INSTALLATION
echo ════════════════════════════════════════════════════════════════
echo.

gcloud --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ gcloud not found in PATH
    echo.
    echo Please:
    echo    1. Close and reopen this terminal
    echo    2. Or restart your computer
    echo    3. Then run this script again
    pause
    exit /b 1
)

echo.
echo ✅ Google Cloud SDK is working!
echo.

echo ════════════════════════════════════════════════════════════════
echo      STEP 2: VERIFY PROJECT
echo ════════════════════════════════════════════════════════════════
echo.

gcloud config get-value project
echo.

echo ════════════════════════════════════════════════════════════════
echo      STEP 3: SET DEFAULT REGION
echo ════════════════════════════════════════════════════════════════
echo.

gcloud config set compute/region us-central1
echo ✅ Default region set to us-central1
echo.

echo ════════════════════════════════════════════════════════════════
echo      STEP 4: ENABLE REQUIRED APIs
echo ════════════════════════════════════════════════════════════════
echo.

echo Enabling Cloud Run API...
gcloud services enable run.googleapis.com
echo.

echo Enabling Cloud Build API...
gcloud services enable cloudbuild.googleapis.com
echo.

echo Enabling Container Registry API...
gcloud services enable containerregistry.googleapis.com
echo.

echo Enabling Cloud SQL Admin API...
gcloud services enable sqladmin.googleapis.com
echo.

echo ✅ All APIs enabled!
echo.

echo ════════════════════════════════════════════════════════════════
echo      ✅ SETUP COMPLETE!
echo ════════════════════════════════════════════════════════════════
echo.
echo 🚀 You're ready to deploy!
echo.
echo Next steps:
echo    1. Set up Cloud SQL database
echo    2. Deploy Django to Cloud Run
echo    3. Connect Firebase to Cloud Run
echo.
echo Run: deploy_to_cloud_run.bat
echo.
pause

