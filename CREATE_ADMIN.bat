@echo off
echo.
echo ========================================
echo   Her Beauty Hub - Create Admin User
echo ========================================
echo.
cd "c:\shiku salon"
echo Changing to project directory...
echo.
echo Follow the prompts to create admin account:
echo.
python manage.py createsuperuser
echo.
echo ========================================
echo   Admin account created successfully!
echo ========================================
echo.
echo You can now login at:
echo   http://127.0.0.1:8000/admin/
echo.
pause

