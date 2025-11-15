@echo off
cls
echo.
echo ================================================================
echo      DEPLOYMENT - USING KNOWN GCLOUD PATH
echo ================================================================
echo.

REM Use the exact path provided
set "GCLOUD=C:\Users\Benson\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

echo Using gcloud at: %GCLOUD%
echo.

REM Verify it works
"%GCLOUD%" --version
if %errorlevel% neq 0 (
    echo [ERROR] gcloud not working
    pause
    exit /b 1
)

echo.
echo [OK] gcloud is working! Starting deployment...
echo.
pause

REM Set as environment variable for the deployment script
set "GCLOUD_CMD=%GCLOUD%"

REM Now call the deployment script
call deploy_complete_with_path.bat

