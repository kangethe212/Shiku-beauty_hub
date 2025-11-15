@echo off
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo      INSTALL GOOGLE CLOUD SDK
echo ════════════════════════════════════════════════════════════════
echo.

echo 📥 Opening Google Cloud SDK download page...
start https://cloud.google.com/sdk/docs/install

echo.
echo ════════════════════════════════════════════════════════════════
echo      INSTALLATION INSTRUCTIONS
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 STEPS:
echo.
echo 1. In the browser that just opened:
echo    • Click "Download Google Cloud SDK"
echo    • Choose "Windows 64-bit" (or your system)
echo    • Download the .exe file
echo.
echo 2. Run the installer:
echo    • Double-click the downloaded .exe file
echo    • Follow the installation wizard
echo    • ✅ Check "Run gcloud init" at the end
echo.
echo 3. After installation:
echo    • Close and reopen this terminal
echo    • Run: gcloud --version (to verify)
echo    • Run: gcloud auth login
echo    • Run: gcloud config set project shiku-beuty-hub
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 TIP: The installer will guide you through:
echo    • Login to Google account
echo    • Select project: shiku-beuty-hub
echo    • Choose region: us-central1
echo.
echo 📖 For detailed instructions, see: INSTALL_GOOGLE_CLOUD_SDK.md
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════
echo      VERIFY INSTALLATION
echo ════════════════════════════════════════════════════════════════
echo.

echo After installation, close and reopen this terminal, then run:
echo.
echo   gcloud --version
echo.
echo If you see version information, installation was successful! ✅
echo.
pause

