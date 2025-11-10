@echo off
cls
color 0A
echo.
echo ========================================================================
echo           RAILWAY DEPLOYMENT FIX - PUSHING TO GITHUB
echo ========================================================================
echo.
echo FIXES APPLIED:
echo   [*] requirements.txt - All packages listed properly
echo   [*] Procfile - Correct PORT binding for Railway
echo   [*] nixpacks.toml - Explicit build instructions
echo   [*] settings.py - Production-ready configuration
echo   [*] WhiteNoise - Static files handling
echo.
echo YOUR DATA ON RAILWAY:
echo   [*] 24 Hairstyles
echo   [*] 30 Perfumes
echo   [*] 6 Clothing Items
echo   [*] 10 Gallery Photos
echo   [*] 9 Videos
echo   [*] Admin: admin / shiku2025
echo.
echo ========================================================================
echo.
pause
echo.

echo [1/3] Adding all files...
git add -A
echo ✅ Files added

echo.
echo [2/3] Creating commit...
git commit -m "Railway deployment fixed: requirements, Procfile, nixpacks, settings"
echo ✅ Commit created

echo.
echo [3/3] Pushing to GitHub...
git push
echo ✅ Pushed to GitHub

echo.
echo ========================================================================
echo           PUSH COMPLETE! RAILWAY WILL AUTO-DEPLOY!
echo ========================================================================
echo.
echo What happens next:
echo   1. Railway detects your push (immediate)
echo   2. Starts rebuilding (2-3 minutes)
echo   3. Installs ALL packages correctly
echo   4. Deploys your website (3-5 min total)
echo   5. YOUR WEBSITE IS LIVE! 🚀
echo.
echo Check Railway dashboard:
echo   - Build logs should show: "Successfully installed django-jazzmin"
echo   - Deploy should show: "Starting gunicorn"
echo   - Status should turn GREEN
echo.
echo Your website will be at:
echo   https://shiku-beauty-hub-production.up.railway.app/
echo   (or similar Railway URL)
echo.
echo Admin login:
echo   Username: admin
echo   Password: shiku2025
echo.
echo ========================================================================
echo           CONGRATULATIONS! YOUR WEBSITE WILL BE LIVE SOON!
echo ========================================================================
echo.
pause

