@echo off
REM This version uses GCLOUD_CMD environment variable if set
REM Otherwise falls back to regular gcloud command

if defined GCLOUD_CMD (
    set "GCLOUD=%GCLOUD_CMD%"
) else (
    set "GCLOUD=gcloud"
)

echo Using gcloud command: %GCLOUD%
echo.

echo ================================================================
echo      STEP 1: SET UP CLOUD SQL DATABASE
echo ================================================================
echo.

set /p create_db="Do you want to create a new Cloud SQL database? (Y/n): "
if /i "%create_db%"=="n" goto skip_db

echo.
echo This will create a PostgreSQL database instance.
echo It may take 5-10 minutes. Please be patient.
echo.
set /p db_root_password="Enter a STRONG password for database root: "
if "%db_root_password%"=="" (
    echo [ERROR] Password cannot be empty!
    pause
    exit /b 1
)

echo.
echo Creating Cloud SQL instance (this takes 5-10 minutes)...
"%GCLOUD%" sql instances create shiku-db ^
  --database-version=POSTGRES_14 ^
  --tier=db-f1-micro ^
  --region=us-central1 ^
  --root-password=%db_root_password%

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Database creation failed or instance already exists.
    echo Continuing with existing database...
) else (
    echo.
    echo [OK] Database instance created!
)

echo.
echo Creating database...
"%GCLOUD%" sql databases create shiku_db --instance=shiku-db 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Database may already exist, continuing...
)

echo.
set /p db_user_password="Enter password for database user 'shiku_user': "
if "%db_user_password%"=="" (
    echo [ERROR] Password cannot be empty!
    pause
    exit /b 1
)

"%GCLOUD%" sql users create shiku_user --instance=shiku-db --password=%db_user_password% 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] User may already exist, continuing...
)

echo.
echo Getting connection name...
for /f "tokens=*" %%i in ('"%GCLOUD%" sql instances describe shiku-db --format="value(connectionName)"') do set CONNECTION_NAME=%%i
echo Connection name: %CONNECTION_NAME%
echo.
echo [IMPORTANT] SAVE THIS CONNECTION NAME: %CONNECTION_NAME%
echo.
pause

:skip_db
echo.
echo Getting existing connection name...
for /f "tokens=*" %%i in ('"%GCLOUD%" sql instances describe shiku-db --format="value(connectionName)"') do set CONNECTION_NAME=%%i
if "%CONNECTION_NAME%"=="" (
    echo [ERROR] Could not get connection name. Please create database first.
    pause
    exit /b 1
)
echo Connection name: %CONNECTION_NAME%
echo.

echo ================================================================
echo      STEP 2: GENERATE SECRET KEY
echo ================================================================
echo.

echo Generating Django secret key...
for /f "tokens=*" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set SECRET_KEY=%%i
echo.
echo Secret Key: %SECRET_KEY%
echo.
echo [IMPORTANT] SAVE THIS SECRET KEY!
echo.
pause

echo ================================================================
echo      STEP 3: BUILD DOCKER IMAGE
echo ================================================================
echo.

echo Building Docker image (this takes 5-10 minutes)...
docker build -t gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build Docker image
    pause
    exit /b 1
)

echo.
echo [OK] Docker image built successfully!
echo.

echo ================================================================
echo      STEP 4: PUSH TO CONTAINER REGISTRY
echo ================================================================
echo.

echo Configuring Docker for Google Cloud...
"%GCLOUD%" auth configure-docker

echo.
echo Pushing image to Google Container Registry...
docker push gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest
if %errorlevel% neq 0 (
    echo [ERROR] Failed to push image
    pause
    exit /b 1
)

echo.
echo [OK] Image pushed successfully!
echo.

echo ================================================================
echo      STEP 5: DEPLOY TO CLOUD RUN
echo ================================================================
echo.

echo Deploying to Cloud Run...
"%GCLOUD%" run deploy shiku-beuty-hub ^
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
  --set-env-vars "SECRET_KEY=%SECRET_KEY%,DEBUG=False" ^
  --add-cloudsql-instances %CONNECTION_NAME%

if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy to Cloud Run
    pause
    exit /b 1
)

echo.
echo [OK] Deployed to Cloud Run!
echo.

for /f "tokens=*" %%i in ('"%GCLOUD%" run services describe shiku-beuty-hub --region us-central1 --format "value(status.url)"') do set CLOUD_RUN_URL=%%i
echo Cloud Run URL: %CLOUD_RUN_URL%
echo.
pause

echo ================================================================
echo      STEP 6: CONFIGURE DATABASE CONNECTION
echo ================================================================
echo.

set /p db_user_password="Enter database user password again: "
set DATABASE_URL=postgresql://shiku_user:%db_user_password%@/shiku_db?host=/cloudsql/%CONNECTION_NAME%

echo.
echo Configuring database connection...
"%GCLOUD%" run services update shiku-beuty-hub ^
  --region us-central1 ^
  --update-env-vars "DATABASE_URL=%DATABASE_URL%"

echo.
echo [OK] Database configured!
echo.

echo ================================================================
echo      STEP 7: RUN MIGRATIONS
echo ================================================================
echo.

echo Creating migration job...
"%GCLOUD%" run jobs create migrate-shiku ^
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest ^
  --region us-central1 ^
  --set-env-vars "SECRET_KEY=%SECRET_KEY%,DEBUG=False" ^
  --set-env-vars "DATABASE_URL=%DATABASE_URL%" ^
  --add-cloudsql-instances %CONNECTION_NAME% ^
  --command python ^
  --args manage.py,migrate 2>nul

echo.
echo Executing migrations...
"%GCLOUD%" run jobs execute migrate-shiku --region us-central1
if %errorlevel% neq 0 (
    echo [WARNING] Migration job may have already been created. Executing existing job...
    "%GCLOUD%" run jobs execute migrate-shiku --region us-central1 --wait
)

echo.
echo [OK] Migrations complete!
echo.
pause

echo ================================================================
echo      STEP 8: CONNECT FIREBASE TO CLOUD RUN
echo ================================================================
echo.

echo Restoring Cloud Run configuration in firebase.json...
copy firebase.json.backup firebase.json

echo.
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo Deploying Firebase Hosting...
firebase deploy --only hosting

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Firebase deployment failed. This might be because:
    echo    1. Cloud Run API not enabled (wait 2-3 more minutes)
    echo    2. Service name mismatch
    echo.
    echo You can deploy manually later with: firebase deploy --only hosting
) else (
    echo.
    echo [OK] Firebase Hosting connected to Cloud Run!
)

echo.
echo ================================================================
echo      DEPLOYMENT COMPLETE!
echo ================================================================
echo.
echo Your website URLs:
echo    Firebase: https://shiku-beuty-hub.web.app
echo    Cloud Run: %CLOUD_RUN_URL%
echo.
echo Next step: Create admin user
echo    Run: deploy_to_cloud_run.bat (option 9)
echo.
pause

