@echo off
cls
echo ========================================================================
echo    PUSHING SHIKU BEAUTY HUB TO GITHUB
echo ========================================================================
echo.

echo Configuring Git...
git config user.email "bennymaish01@gmail.com"
git config user.name "Shiku Beauty Hub"

echo.
echo Adding files...
git add .

echo.
echo Creating commit...
git commit -m "Initial commit: Shiku Beauty Hub complete website"

echo.
echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
echo You will need to enter your GitHub credentials:
echo Username: kangethe212
echo Password: Use your Personal Access Token (get from github.com/settings/tokens)
echo.
git push -u origin main

echo.
echo ========================================================================
echo    PUSH COMPLETE!
echo ========================================================================
echo.
echo Visit: https://github.com/kangethe212/Shiku-beauty_hub
echo.
pause

