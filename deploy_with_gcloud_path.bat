@echo off
cls
echo.
echo ================================================================
echo      DEPLOYMENT - USING FULL GCLOUD PATH
echo ================================================================
echo.

REM Try to find and use gcloud with full path
set "GCLOUD_CMD="

if exist "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD_CMD=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
) else if exist "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD_CMD=C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
) else if exist "%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD_CMD=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
) else (
    echo [ERROR] Could not find gcloud
    echo.
    echo Please provide the full path to gcloud.cmd
    echo Or close and reopen terminal after installing gcloud
    pause
    exit /b 1
)

echo [OK] Using gcloud at: %GCLOUD_CMD%
echo.

REM Test gcloud
"%GCLOUD_CMD%" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] gcloud not working at that location
    pause
    exit /b 1
)

echo [OK] gcloud is working!
echo.

echo ================================================================
echo      STARTING DEPLOYMENT
echo ================================================================
echo.

REM Set GCLOUD_CMD as environment variable for deploy_complete.bat
set "GCLOUD_CMD=%GCLOUD_CMD%"

REM Now call deploy script with gcloud path
call deploy_complete_with_path.bat

