@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      SHIKU BEAUTY HUB - FIREBASE DEPLOYMENT HELPER
echo ════════════════════════════════════════════════════════════════
echo.
echo This script will help you deploy to Firebase step by step.
echo.
echo 📋 PREREQUISITES CHECK:
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK not found!
    echo    Please install from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
) else (
    echo ✅ Google Cloud SDK found
)

REM Check if firebase is installed
where firebase >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found!
    echo    Please install: npm install -g firebase-tools
    pause
    exit /b 1
) else (
    echo ✅ Firebase CLI found
)

REM Check if docker is installed
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found!
    echo    Please install from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
) else (
    echo ✅ Docker found
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo Choose an action:
echo.
echo 1. Login to Google Cloud
echo 2. Login to Firebase
echo 3. Set up Google Cloud Project
echo 4. Build Docker Image
echo 5. Deploy to Cloud Run
echo 6. Collect Static Files
echo 7. Deploy Firebase Hosting
echo 8. Full Deployment (Steps 4-7)
echo 9. View Cloud Run Logs
echo 0. Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto login_gcloud
if "%choice%"=="2" goto login_firebase
if "%choice%"=="3" goto setup_project
if "%choice%"=="4" goto build_docker
if "%choice%"=="5" goto deploy_cloudrun
if "%choice%"=="6" goto collect_static
if "%choice%"=="7" goto deploy_firebase
if "%choice%"=="8" goto full_deploy
if "%choice%"=="9" goto view_logs
if "%choice%"=="0" goto end
goto invalid

:login_gcloud
echo.
echo 🔐 Logging in to Google Cloud...
gcloud auth login
goto end

:login_firebase
echo.
echo 🔐 Logging in to Firebase...
firebase login
goto end

:setup_project
echo.
echo ⚙️ Setting up Google Cloud Project...
echo.
set /p project_id="Enter Project ID (e.g., shiku-beauty-hub): "
if "%project_id%"=="" (
    echo ❌ Project ID cannot be empty!
    pause
    goto end
)
echo.
echo Creating project: %project_id%
gcloud projects create %project_id% --name="Shiku Beauty Hub"
if %errorlevel% neq 0 (
    echo ⚠️ Project might already exist, continuing...
)
echo.
echo Setting current project...
gcloud config set project %project_id%
echo.
echo Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable sqladmin.googleapis.com
echo.
echo ✅ Project setup complete!
pause
goto end

:build_docker
echo.
echo 🐳 Building Docker image...
echo.
docker build -t gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest .
if %errorlevel% neq 0 (
    echo ❌ Error building Docker image!
    pause
    goto end
)
echo.
echo ✅ Docker image built successfully!
echo.
echo 📤 Pushing to Google Container Registry...
gcloud auth configure-docker
docker push gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest
if %errorlevel% neq 0 (
    echo ❌ Error pushing image!
    pause
    goto end
)
echo.
echo ✅ Image pushed successfully!
pause
goto end

:deploy_cloudrun
echo.
echo 🚢 Deploying to Cloud Run...
echo.
echo ⚠️ Make sure you have:
echo    - Secret key ready
echo    - Database connection name ready
echo.
set /p secret_key="Enter SECRET_KEY: "
if "%secret_key%"=="" (
    echo ❌ Secret key cannot be empty!
    pause
    goto end
)
set /p connection_name="Enter Cloud SQL connection name (PROJECT_ID:REGION:INSTANCE): "
if "%connection_name%"=="" (
    echo ❌ Connection name cannot be empty!
    pause
    goto end
)
echo.
echo Deploying...
gcloud run deploy shiku-beuty-hub ^
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --port 8080 ^
  --memory 512Mi ^
  --cpu 1 ^
  --min-instances 0 ^
  --max-instances 10 ^
  --timeout 300 ^
  --set-env-vars "SECRET_KEY=%secret_key%,DEBUG=False" ^
  --add-cloudsql-instances %connection_name%
if %errorlevel% neq 0 (
    echo ❌ Error deploying to Cloud Run!
    pause
    goto end
)
echo.
echo ✅ Deployed to Cloud Run successfully!
echo.
echo Getting service URL...
gcloud run services describe shiku-beuty-hub --region us-central1 --format "value(status.url)"
pause
goto end

:collect_static
echo.
echo 📦 Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ❌ Error collecting static files!
    pause
    goto end
)
echo.
echo ✅ Static files collected!
pause
goto end

:deploy_firebase
echo.
echo 🔥 Deploying Firebase Hosting...
firebase deploy --only hosting
if %errorlevel% neq 0 (
    echo ❌ Error deploying Firebase Hosting!
    pause
    goto end
)
echo.
echo ✅ Firebase Hosting deployed successfully!
echo.
echo 🌐 Your website should be live now!
pause
goto end

:full_deploy
echo.
echo 🚀 Starting full deployment...
echo.
call :build_docker
if %errorlevel% neq 0 goto end
call :collect_static
if %errorlevel% neq 0 goto end
call :deploy_firebase
if %errorlevel% neq 0 goto end
echo.
echo ✅ Full deployment complete!
pause
goto end

:view_logs
echo.
echo 📊 Viewing Cloud Run logs...
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format json
pause
goto end

:invalid
echo.
echo ❌ Invalid choice!
pause
goto end

:end
echo.
echo ════════════════════════════════════════════════════════════════
echo.
exit /b 0

