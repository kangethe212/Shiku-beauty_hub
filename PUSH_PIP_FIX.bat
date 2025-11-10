@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      RAILWAY PIP FIX - PUSHING NOW
echo ════════════════════════════════════════════════════════════════
echo.
echo FIX: Changed "pip" to "python -m pip" in nixpacks.toml and Procfile
echo REASON: Railway couldn't find pip command
echo RESULT: Will install all packages correctly!
echo.
echo ════════════════════════════════════════════════════════════════
pause
echo.

git add nixpacks.toml Procfile

git commit -m "Fixed pip command for Railway"

git push

echo.
echo ════════════════════════════════════════════════════════════════
echo      PUSHED! RAILWAY IS REDEPLOYING!
echo ════════════════════════════════════════════════════════════════
echo.
echo Check Railway dashboard in 3-5 minutes!
echo Your website should deploy successfully now!
echo.
pause

