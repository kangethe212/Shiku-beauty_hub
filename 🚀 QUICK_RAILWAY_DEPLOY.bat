@echo off
cls
echo.
echo ================================================================
echo      DEPLOY TO RAILWAY - FREE HOSTING!
echo ================================================================
echo.

echo Railway is the BEST free option for Django!
echo.
echo Benefits:
echo   - Completely FREE ($5/month credit)
echo   - No credit card required
echo   - PostgreSQL included (free)
echo   - Automatic deployments
echo   - Takes 5 minutes
echo   - Already configured in your project!
echo.
pause

echo.
echo ================================================================
echo      STEP 1: CHECK GIT STATUS
echo ================================================================
echo.

git status
echo.

set /p push="Do you want to push to GitHub? (Y/n): "
if /i "%push%"=="n" goto skip_push

echo.
echo Pushing to GitHub...
git add .
git commit -m "Ready for Railway deployment" 2>nul
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Git push failed or not configured
    echo You can push manually or deploy directly from Railway
)

:skip_push
echo.
echo ================================================================
echo      STEP 2: DEPLOY TO RAILWAY
echo ================================================================
echo.

echo Opening Railway in browser...
start https://railway.app

echo.
echo INSTRUCTIONS:
echo.
echo 1. Sign up/Login with GitHub
echo 2. Click "New Project"
echo 3. Select "Deploy from GitHub repo"
echo 4. Choose your repository
echo 5. Railway will auto-deploy!
echo.
echo That's it! Takes 5 minutes!
echo.
echo Your project is already configured with:
echo   - Procfile (deployment config)
echo   - railway.json (Railway settings)
echo   - requirements.txt (dependencies)
echo.
pause

echo.
echo ================================================================
echo      AFTER DEPLOYMENT
echo ================================================================
echo.

echo Once deployed, Railway will give you a URL like:
echo   https://your-app-name.up.railway.app
echo.
echo To create admin user:
echo   railway run python manage.py createsuperuser
echo.
echo To view logs:
echo   railway logs
echo.
echo For more info, see: 🚂 DEPLOY_TO_RAILWAY.md
echo.
pause

