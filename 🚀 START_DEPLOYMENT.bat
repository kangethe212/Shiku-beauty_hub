@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      🚀 STARTING DEPLOYMENT - LET'S GO!
echo ════════════════════════════════════════════════════════════════
echo.

REM Check Docker
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found!
    pause
    exit /b 1
) else (
    echo ✅ Docker: Ready
)

REM Check Firebase
where firebase >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found!
    pause
    exit /b 1
) else (
    echo ✅ Firebase CLI: Ready
)

REM Check gcloud
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Google Cloud SDK not found in PATH
    echo.
    echo Let's try to find it...
    
    REM Try common installation paths
    if exist "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
        set "GCLOUD_PATH=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
        echo ✅ Found gcloud at: %GCLOUD_PATH%
        set "PATH=%PATH%;%GCLOUD_PATH%"
    ) else if exist "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
        set "GCLOUD_PATH=C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin"
        echo ✅ Found gcloud at: %GCLOUD_PATH%
        set "PATH=%PATH%;%GCLOUD_PATH%"
    ) else if exist "%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
        set "GCLOUD_PATH=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin"
        echo ✅ Found gcloud at: %GCLOUD_PATH%
        set "PATH=%PATH%;%GCLOUD_PATH%"
    ) else (
        echo.
        echo ❌ Could not find gcloud automatically
        echo.
        echo Please:
        echo    1. Close and reopen this terminal
        echo    2. Or restart your computer
        echo    3. Then run this script again
        echo.
        echo If gcloud is installed, you can also run commands manually
        echo from the terminal where gcloud init was run.
        echo.
        pause
        exit /b 1
    )
)

REM Verify gcloud works now
gcloud --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ gcloud still not working
    echo    Please close and reopen terminal, then try again
    pause
    exit /b 1
)

echo ✅ Google Cloud SDK: Ready
echo.

echo ════════════════════════════════════════════════════════════════
echo      ✅ ALL PREREQUISITES MET!
echo ════════════════════════════════════════════════════════════════
echo.
echo Ready to deploy! This will:
echo   • Set up Cloud SQL database (5-10 min)
echo   • Build Docker image (5-10 min)
echo   • Deploy to Cloud Run (2-3 min)
echo   • Connect Firebase to Cloud Run
echo.
echo Total time: ~15-20 minutes
echo.
pause

call deploy_complete.bat

