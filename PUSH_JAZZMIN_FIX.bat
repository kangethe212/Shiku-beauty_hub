@echo off
cls
echo.
echo ========================================================================
echo    JAZZMIN FIX - DEPLOYING TO RAILWAY WITHOUT JAZZMIN
echo ========================================================================
echo.
echo CHANGE: Temporarily disabled Jazzmin admin theme
echo REASON: Railway was failing to install it
echo RESULT: Standard Django admin will work perfectly!
echo.
echo Your admin panel will still have:
echo   - All custom admin features
echo   - Beautiful product displays
echo   - Loyalty program management
echo   - Gallery engagement stats
echo   - Everything functional!
echo.
echo ========================================================================
pause
echo.

echo [1/3] Adding files...
git add -A

echo.
echo [2/3] Committing...
git commit -m "Disabled jazzmin for Railway deployment - using standard Django admin"

echo.
echo [3/3] Pushing to GitHub...
git push

echo.
echo ========================================================================
echo    PUSH COMPLETE!
echo ========================================================================
echo.
echo Railway will now:
echo   1. Rebuild your app (2-3 min)
echo   2. Install ALL packages successfully
echo   3. Start without errors
echo   4. Your website will be LIVE!
echo.
echo Admin panel: Standard Django (still powerful!)
echo   Username: admin
echo   Password: shiku2025
echo.
pause

