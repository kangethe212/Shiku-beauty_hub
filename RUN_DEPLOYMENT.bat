@echo off
cls
echo.
echo ================================================================
echo      DEPLOYMENT - FINDING GCLOUD
echo ================================================================
echo.

REM Try common gcloud locations
set "GCLOUD_PATH="

if exist "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD_PATH=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    goto found
)
if exist "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD_PATH=C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    goto found
)
if exist "%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD_PATH=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    goto found
)

echo [ERROR] Could not find gcloud automatically
echo.
echo Please do ONE of the following:
echo.
echo Option 1: Close and reopen terminal, then run this script again
echo Option 2: Tell me where gcloud is installed
echo Option 3: Run gcloud commands from the terminal where you ran gcloud init
echo.
pause
exit /b 1

:found
echo [OK] Found gcloud at: %GCLOUD_PATH%
echo.

REM Test it
"%GCLOUD_PATH%" --version
if %errorlevel% neq 0 (
    echo [ERROR] gcloud not working at that location
    pause
    exit /b 1
)

echo.
echo [OK] gcloud is working! Starting deployment...
echo.
pause

REM Add to PATH for this session
set "PATH=%PATH%;%~dp0"
set "GCLOUD=%GCLOUD_PATH%"

REM Call deployment with gcloud path
call deploy_complete_with_path.bat

