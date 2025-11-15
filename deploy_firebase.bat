@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      SHIKU BEAUTY HUB - FIREBASE + CLOUD RUN DEPLOYMENT
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 PREREQUISITES:
echo    ✅ Google Cloud account (billing enabled)
echo    ✅ Firebase account
echo    ✅ gcloud CLI installed
echo    ✅ firebase CLI installed
echo    ✅ Docker installed
echo.
pause

echo.
echo 📦 STEP 1: Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ❌ Error collecting static files!
    pause
    exit /b 1
)

echo.
echo 🐳 STEP 2: Building Docker image...
docker build -t gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest .
if %errorlevel% neq 0 (
    echo ❌ Error building Docker image!
    pause
    exit /b 1
)

echo.
echo 📤 STEP 3: Pushing to Google Container Registry...
docker push gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest
if %errorlevel% neq 0 (
    echo ❌ Error pushing image!
    pause
    exit /b 1
)

echo.
echo 🚢 STEP 4: Deploying to Cloud Run...
echo    ⚠️  Make sure to set your SECRET_KEY and DATABASE_URL!
echo.
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
  --timeout 300

if %errorlevel% neq 0 (
    echo ❌ Error deploying to Cloud Run!
    pause
    exit /b 1
)

echo.
echo 🔥 STEP 5: Deploying Firebase Hosting...
firebase deploy --only hosting
if %errorlevel% neq 0 (
    echo ❌ Error deploying Firebase Hosting!
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════
echo      ✅ DEPLOYMENT COMPLETE!
echo ════════════════════════════════════════════════════════════════
echo.
echo 🌐 Your website is now live!
echo    Check Firebase Console for your URL:
echo    https://console.firebase.google.com/
echo.
echo 💡 Don't forget to:
echo    1. Run migrations: gcloud run jobs execute migrate-shiku
echo    2. Create admin user
echo    3. Transfer data from Railway
echo.
pause

