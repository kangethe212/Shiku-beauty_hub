@echo off
echo ============================================================
echo   QUICK FIX FOR 500 ERROR ON RAILWAY
echo ============================================================
echo.
echo This script will help you fix the 500 error.
echo.
echo STEP 1: Check Railway Logs
echo   - Go to Railway dashboard
echo   - Click your service
echo   - View Logs tab
echo   - Look for error messages
echo.
echo STEP 2: Most Common Fixes
echo.
echo Option A: Using Railway Web Terminal
echo   1. Railway dashboard ^> Your service ^> Deployments
echo   2. Click latest deployment ^> View Logs/Open Terminal
echo   3. Run these commands:
echo.
echo      python manage.py migrate
echo      python manage.py collectstatic --noinput
echo.
echo Option B: Using Railway CLI
echo   1. Install: npm i -g @railway/cli
echo   2. Run:
echo      railway login
echo      railway link
echo      railway run python manage.py migrate
echo      railway run python manage.py collectstatic --noinput
echo.
echo STEP 3: Add Environment Variables
echo   Railway dashboard ^> Settings ^> Variables
echo   Add:
echo   - SECRET_KEY (generate one)
echo   - DEBUG = False
echo.
echo ============================================================
echo   MOST COMMON ISSUE: Missing Migrations
echo ============================================================
echo.
echo Run this first:
echo   railway run python manage.py migrate
echo.
echo ============================================================
pause

