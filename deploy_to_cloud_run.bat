@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      DEPLOY DJANGO TO GOOGLE CLOUD RUN
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK not found!
    echo.
    echo Please install from: https://cloud.google.com/sdk/docs/install
    echo.
    pause
    exit /b 1
)

echo ✅ Google Cloud SDK found
echo.

REM Check if docker is installed
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found!
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo ✅ Docker found
echo.

echo ════════════════════════════════════════════════════════════════
echo.
echo This script will help you deploy to Cloud Run step by step.
echo.
echo Choose an action:
echo.
echo 1. Login to Google Cloud
echo 2. Set up Cloud SQL Database
echo 3. Generate Secret Key
echo 4. Build Docker Image
echo 5. Push to Container Registry
echo 6. Deploy to Cloud Run
echo 7. Configure Database
echo 8. Run Migrations
echo 9. Create Admin User
echo 10. Full Deployment (Steps 4-9)
echo 0. Exit
echo.
set /p choice="Enter your choice (0-10): "

if "%choice%"=="1" goto login_gcloud
if "%choice%"=="2" goto setup_database
if "%choice%"=="3" goto generate_secret
if "%choice%"=="4" goto build_docker
if "%choice%"=="5" goto push_docker
if "%choice%"=="6" goto deploy_cloudrun
if "%choice%"=="7" goto config_database
if "%choice%"=="8" goto run_migrations
if "%choice%"=="9" goto create_admin
if "%choice%"=="10" goto full_deploy
if "%choice%"=="0" goto end
goto invalid

:login_gcloud
echo.
echo 🔐 Logging in to Google Cloud...
gcloud auth login
gcloud config set project shiku-beuty-hub
goto end

:setup_database
echo.
echo 📊 Setting up Cloud SQL Database...
echo.
echo ⚠️  This will create a PostgreSQL database instance.
echo    It may take 5-10 minutes.
echo.
set /p db_password="Enter a strong password for database root: "
if "%db_password%"=="" (
    echo ❌ Password cannot be empty!
    pause
    goto end
)
echo.
echo Creating Cloud SQL instance...
gcloud sql instances create shiku-db ^
  --database-version=POSTGRES_14 ^
  --tier=db-f1-micro ^
  --region=us-central1 ^
  --root-password=%db_password%
if %errorlevel% neq 0 (
    echo ❌ Failed to create database instance
    pause
    goto end
)
echo.
echo Creating database...
gcloud sql databases create shiku_db --instance=shiku-db
echo.
set /p user_password="Enter password for database user: "
gcloud sql users create shiku_user ^
  --instance=shiku-db ^
  --password=%user_password%
echo.
echo ✅ Database setup complete!
echo.
echo Connection name:
gcloud sql instances describe shiku-db --format="value(connectionName)"
echo.
pause
goto end

:generate_secret
echo.
echo 🔑 Generating Django secret key...
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
echo.
echo 💾 Copy and save this secret key!
pause
goto end

:build_docker
echo.
echo 🐳 Building Docker image...
echo    This may take 5-10 minutes...
docker build -t gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest .
if %errorlevel% neq 0 (
    echo ❌ Failed to build Docker image
    pause
    goto end
)
echo.
echo ✅ Docker image built successfully!
pause
goto end

:push_docker
echo.
echo 📤 Pushing to Google Container Registry...
gcloud auth configure-docker
docker push gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest
if %errorlevel% neq 0 (
    echo ❌ Failed to push image
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
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest ^
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
    echo ❌ Failed to deploy
    pause
    goto end
)
echo.
echo ✅ Deployed successfully!
echo.
echo Service URL:
gcloud run services describe shiku-beuty-hub --region us-central1 --format "value(status.url)"
pause
goto end

:config_database
echo.
echo ⚙️  Configuring database connection...
set /p db_password="Enter database user password: "
set /p connection_name="Enter connection name: "
gcloud run services update shiku-beuty-hub ^
  --region us-central1 ^
  --update-env-vars "DATABASE_URL=postgresql://shiku_user:%db_password%@/shiku_db?host=/cloudsql/%connection_name%"
echo.
echo ✅ Database configured!
pause
goto end

:run_migrations
echo.
echo 📦 Running migrations...
set /p secret_key="Enter SECRET_KEY: "
set /p db_url="Enter DATABASE_URL: "
set /p connection_name="Enter connection name: "
gcloud run jobs create migrate-shiku ^
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest ^
  --region us-central1 ^
  --set-env-vars "SECRET_KEY=%secret_key%,DEBUG=False" ^
  --set-env-vars "DATABASE_URL=%db_url%" ^
  --add-cloudsql-instances %connection_name% ^
  --command python ^
  --args manage.py,migrate
echo.
echo Executing migration...
gcloud run jobs execute migrate-shiku --region us-central1
echo.
echo ✅ Migrations complete!
pause
goto end

:create_admin
echo.
echo 👤 Creating admin user...
set /p secret_key="Enter SECRET_KEY: "
set /p db_url="Enter DATABASE_URL: "
set /p connection_name="Enter connection name: "
gcloud run jobs create createsuperuser-shiku ^
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest ^
  --region us-central1 ^
  --set-env-vars "SECRET_KEY=%secret_key%,DEBUG=False" ^
  --set-env-vars "DATABASE_URL=%db_url%" ^
  --add-cloudsql-instances %connection_name% ^
  --command python ^
  --args manage.py,createsuperuser ^
  --interactive
echo.
echo Executing...
gcloud run jobs execute createsuperuser-shiku --region us-central1
echo.
echo ✅ Admin user creation complete!
pause
goto end

:full_deploy
echo.
echo 🚀 Starting full deployment...
echo.
echo This will:
echo   1. Build Docker image
echo   2. Push to registry
echo   3. Deploy to Cloud Run
echo.
echo Make sure you have:
echo   - Secret key ready
echo   - Database connection name ready
echo   - Database password ready
echo.
pause
call :build_docker
call :push_docker
call :deploy_cloudrun
echo.
echo ✅ Full deployment complete!
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
exit /b 0

