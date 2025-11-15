@echo off
cls
echo.
echo ================================================================
echo      DEPLOYMENT STATUS CHECK
echo ================================================================
echo.

set "GCLOUD=C:\Users\Benson\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

echo [1] Checking gcloud...
"%GCLOUD%" --version
if %errorlevel% equ 0 (
    echo [OK] gcloud is working
) else (
    echo [ERROR] gcloud not working
    pause
    exit /b 1
)

echo.
echo [2] Checking project...
"%GCLOUD%" config get-value project
echo.

echo [3] Checking Cloud SQL instances...
"%GCLOUD%" sql instances list
echo.

echo [4] Checking Cloud Run services...
"%GCLOUD%" run services list --region=us-central1
echo.

echo [5] Checking Firebase deployment...
firebase projects:list | findstr shiku-beuty-hub
echo.

echo ================================================================
echo      STATUS SUMMARY
echo ================================================================
echo.
echo If you see database/Cloud Run services listed above,
echo deployment has started. If not, run DEPLOY_NOW.bat
echo.
pause

