@echo off
echo ======================================================================
echo    PUSHING SHIKU BEAUTY HUB TO GITHUB
echo ======================================================================
echo.

echo Step 1: Adding all files...
git add .

echo.
echo Step 2: Creating commit...
git commit -m "Initial commit: Shiku Beauty Hub - Complete beauty e-commerce website with 60 products, stunning animations, WhatsApp integration, Jazzmin admin, and notification system"

echo.
echo Step 3: Adding remote repository...
git remote add origin https://github.com/kangethe212/Shiku-beauty_hub.git 2>nul

echo.
echo Step 4: Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ======================================================================
echo    PUSH COMPLETE!
echo ======================================================================
echo.
echo Your code is now on GitHub:
echo https://github.com/kangethe212/Shiku-beauty_hub
echo.
pause

