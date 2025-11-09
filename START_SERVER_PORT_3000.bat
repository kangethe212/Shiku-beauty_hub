@echo off
cls
echo.
echo ========================================
echo   Her Beauty Hub - Starting Server
echo   PORT 3000
echo ========================================
echo.
cd "c:\shiku salon"
echo [1/2] Navigating to project directory...
echo Current: %CD%
echo.
echo [2/2] Starting Django server on port 3000...
echo.
echo ========================================
echo.
echo Your website will be available at:
echo.
echo   http://127.0.0.1:3000/
echo.
echo Admin panel at:
echo   http://127.0.0.1:3000/admin/
echo.
echo ========================================
echo Starting server...
echo.
python manage.py runserver 3000
echo.
pause


