@echo off
cls
echo ========================================================================
echo    PUSHING NEW FEATURES TO GITHUB
echo ========================================================================
echo.
echo NEW FEATURES BEING PUSHED:
echo   - Loyalty Program (points, discounts, referrals, wishlist)
echo   - Gallery Likes and Comments
echo   - PostgreSQL Database Configuration
echo   - User Authentication System
echo   - Customer Dashboard
echo.
echo ========================================================================
echo.

echo Adding files...
git add .

echo.
echo Creating commit...
git commit -m "Added loyalty program, gallery engagement, and PostgreSQL support"

echo.
echo Pushing to GitHub...
git push

echo.
echo ========================================================================
echo    PUSH COMPLETE!
echo ========================================================================
echo.
echo View at: https://github.com/kangethe212/Shiku-beauty_hub
echo.
pause

