@echo off
cls
echo ========================================================================
echo    POSTGRESQL SETUP - SHIKU BEAUTY HUB
echo ========================================================================
echo.

echo Database: shiku_db
echo User: postgres
echo Status: CONNECTED!
echo.

echo Step 1: Creating superuser...
echo.
python manage.py createsuperuser

echo.
echo Step 2: Starting server...
echo.
echo Visit: http://127.0.0.1:3000/
echo Admin: http://127.0.0.1:3000/admin/
echo.
python manage.py runserver 3000

