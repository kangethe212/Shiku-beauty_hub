@echo off
cls
echo.
echo ================================================================
echo      STARTING DEPLOYMENT - LET'S GO!
echo ================================================================
echo.

REM Check Docker
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found!
    pause
    exit /b 1
) else (
    echo [OK] Docker: Ready
)

REM Check Firebase
where firebase >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Firebase CLI not found!
    pause
    exit /b 1
) else (
    echo [OK] Firebase CLI: Ready
)

REM Check gcloud - try to find it
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Google Cloud SDK not in PATH
    echo Trying to locate gcloud...
    
    if exist "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
        set "GCLOUD_PATH=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
        set "PATH=%PATH%;%GCLOUD_PATH%"
        echo [OK] Found gcloud!
    ) else if exist "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
        set "GCLOUD_PATH=C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin"
        set "PATH=%PATH%;%GCLOUD_PATH%"
        echo [OK] Found gcloud!
    ) else if exist "%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
        set "GCLOUD_PATH=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin"
        set "PATH=%PATH%;%GCLOUD_PATH%"
        echo [OK] Found gcloud!
    ) else (
        echo.
        echo [ERROR] Could not find gcloud
        echo.
        echo Please close and reopen terminal, then try again.
        echo Or run gcloud commands from the terminal where you ran gcloud init.
        echo.
        pause
        exit /b 1
    )
)

REM Verify
gcloud --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] gcloud still not working
    echo Please close and reopen terminal
    pause
    exit /b 1
)

echo [OK] Google Cloud SDK: Ready
echo.

echo ================================================================
echo      ALL PREREQUISITES MET - STARTING DEPLOYMENT!
echo ================================================================
echo.
echo This will take 15-20 minutes total.
echo.
pause

call deploy_complete.bat

