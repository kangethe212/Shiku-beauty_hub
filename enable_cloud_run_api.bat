@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      ENABLE CLOUD RUN API FOR FIREBASE HOSTING
echo ════════════════════════════════════════════════════════════════
echo.

echo 📋 INSTRUCTIONS:
echo.
echo 1. Open this link in your browser:
echo.
echo    https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=140804076783
echo.
echo 2. Click the "ENABLE" button
echo.
echo 3. Wait 2-3 minutes for activation
echo.
echo 4. Come back here and press any key to continue...
echo.
pause

echo.
echo 🔍 Checking if Google Cloud SDK is installed...
where gcloud >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Google Cloud SDK found!
    echo.
    echo Attempting to enable via command line...
    echo.
    gcloud auth login
    gcloud config set project shiku-beuty-hub
    gcloud services enable run.googleapis.com
    echo.
    echo ✅ Cloud Run API enabled!
    echo.
    echo Waiting 30 seconds for activation...
    timeout /t 30 /nobreak
) else (
    echo ⚠️  Google Cloud SDK not installed
    echo.
    echo Please enable the API via the web console link above.
    echo.
    echo After enabling, wait 2-3 minutes, then run:
    echo    firebase deploy --only hosting
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 📝 Next Steps:
echo    1. Make sure API is enabled (check web console)
echo    2. Wait 2-3 minutes
echo    3. Run: firebase deploy --only hosting
echo.
pause

