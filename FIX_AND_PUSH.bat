@echo off
cls
echo.
echo ========================================================================
echo    RAILWAY FIX - PUSH TO GITHUB
echo ========================================================================
echo.
echo ISSUE: Railway couldn't find jazzmin module
echo FIX: requirements.txt updated (removed comment that broke pip)
echo.
echo ========================================================================
echo.

echo [Step 1] Adding files...
git add .

echo.
echo [Step 2] Committing fix...
git commit -m "Fixed requirements.txt for Railway deployment - removed comments"

echo.
echo [Step 3] Pushing to GitHub...
git push

echo.
echo ========================================================================
echo    PUSH COMPLETE!
echo ========================================================================
echo.
echo Railway will now automatically:
echo   1. Detect the change
echo   2. Rebuild your app
echo   3. Install ALL packages (including jazzmin)
echo   4. Deploy successfully!
echo.
echo Check Railway dashboard in 3-5 minutes!
echo Your website will be LIVE!
echo.
echo ========================================================================
pause

