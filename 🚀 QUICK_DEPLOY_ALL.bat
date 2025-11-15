@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      🚀 QUICK DEPLOY - ALL STEPS AUTOMATED
echo ════════════════════════════════════════════════════════════════
echo.

echo This script will:
echo   1. Set up Cloud SQL database
echo   2. Generate secret key
echo   3. Build and push Docker image
echo   4. Deploy to Cloud Run
echo   5. Configure database
echo   6. Run migrations
echo   7. Connect Firebase to Cloud Run
echo.
echo ⚠️  This will take 15-20 minutes total
echo.
pause

call deploy_complete.bat

