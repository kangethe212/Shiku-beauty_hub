@echo off
cls
echo.
echo ================================================================
echo      DEPLOY TO RAILWAY - LET'S GO!
echo ================================================================
echo.

echo [1] Checking git status...
git status
echo.

set /p push="Push changes to GitHub? (Y/n): "
if /i "%push%"=="n" goto skip_push

echo.
echo [2] Adding all files...
git add -A

echo.
echo [3] Committing changes...
git commit -m "Ready for Railway deployment" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] No changes to commit or commit failed
)

echo.
echo [4] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Push failed. You may need to:
    echo   1. Set up GitHub remote
    echo   2. Or deploy directly from Railway
    echo.
    pause
)

:skip_push
echo.
echo ================================================================
echo      DEPLOY TO RAILWAY
echo ================================================================
echo.

echo Opening Railway in browser...
start https://railway.app

echo.
echo ================================================================
echo      RAILWAY DEPLOYMENT STEPS
echo ================================================================
echo.

echo STEP 1: Sign up/Login
echo   - Use GitHub to sign in (easiest)
echo   - Authorize Railway
echo.

echo STEP 2: Create New Project
echo   - Click "New Project"
echo   - Select "Deploy from GitHub repo"
echo   - Choose your repository
echo.

echo STEP 3: Railway Auto-Deploys!
echo   - Railway detects Django automatically
echo   - Sets up PostgreSQL automatically
echo   - Deploys your app
echo   - Gives you a URL
echo.

echo STEP 4: Set Environment Variables (if needed)
echo   - SECRET_KEY (generate one)
echo   - DEBUG=False
echo.

echo STEP 5: Create Admin User
echo   - Go to Railway dashboard
echo   - Click on your service
echo   - Open terminal
echo   - Run: python manage.py createsuperuser
echo.

echo ================================================================
echo      YOUR PROJECT IS READY!
echo ================================================================
echo.

echo Files configured:
echo   - Procfile (deployment command)
echo   - railway.json (Railway settings)
echo   - requirements.txt (dependencies)
echo   - settings.py (Railway database config)
echo.

echo After deployment, your site will be at:
echo   https://your-app-name.up.railway.app
echo.

echo ================================================================
echo.

pause

