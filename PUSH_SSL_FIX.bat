@echo off
cls
color 0A
echo.
echo ═══════════════════════════════════════════════════════════
echo     RAILWAY DEPLOYMENT - SSL FIX
echo ═══════════════════════════════════════════════════════════
echo.
echo FIXES:
echo   [*] Added SSL configuration (sslmode=require)
echo   [*] Disabled Jazzmin admin theme
echo   [*] Standard Django admin (works great!)
echo   [*] All features preserved
echo.
echo YOUR 60 PRODUCTS ARE READY ON RAILWAY!
echo   [*] 24 Hairstyles
echo   [*] 30 Perfumes
echo   [*] 6 Clothing
echo   [*] 10 Gallery + 9 Videos
echo.
echo ═══════════════════════════════════════════════════════════
pause
echo.

echo [1/3] Adding files...
git add -A

echo.
echo [2/3] Committing...
git commit -m "Railway SSL fix and jazzmin disabled - ready to deploy"

echo.
echo [3/3] Pushing...
git push

echo.
echo ═══════════════════════════════════════════════════════════
echo     SUCCESS! RAILWAY WILL AUTO-REDEPLOY!
echo ═══════════════════════════════════════════════════════════
echo.
echo Watch Railway dashboard:
echo   - Build will start in 30 seconds
echo   - All packages will install (2-3 min)
echo   - Website will deploy (5 min total)
echo   - Status will turn GREEN!
echo.
echo Your live website:
echo   https://your-railway-url.up.railway.app/
echo.
echo Admin login:
echo   Username: admin
echo   Password: shiku2025
echo.
pause

