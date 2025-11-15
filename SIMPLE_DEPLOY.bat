@echo off
REM Simple deployment that uses full path to gcloud

echo.
echo ================================================================
echo      SIMPLE DEPLOYMENT
echo ================================================================
echo.

REM Find gcloud
set "GCLOUD="
if exist "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
) else if exist "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD=C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
) else if exist "%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" (
    set "GCLOUD=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
)

if "%GCLOUD%"=="" (
    echo ERROR: Could not find gcloud
    echo.
    echo SOLUTION: Close and reopen terminal, then try again
    echo Or run from the terminal where you ran: gcloud init
    pause
    exit /b 1
)

echo Using: %GCLOUD%
echo.

REM Now use %GCLOUD% instead of gcloud in all commands
REM For now, let's just test it works
"%GCLOUD%" --version
if %errorlevel% neq 0 (
    echo ERROR: gcloud not working
    pause
    exit /b 1
)

echo.
echo SUCCESS! gcloud is working.
echo.
echo Now you can either:
echo   1. Close and reopen terminal (recommended)
echo   2. Run: deploy_complete_with_path.bat
echo   3. Or continue manually with the guide
echo.
pause

