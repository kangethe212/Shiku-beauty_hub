@echo off
echo ============================================================
echo   TRANSFERRING DATA TO RAILWAY POSTGRESQL
echo ============================================================
echo.

echo Step 1: Setting DATABASE_URL environment variable...
set DATABASE_URL=postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway

echo Step 2: Running migrations on Railway database...
python manage.py migrate --database=default

echo.
echo Step 3: Exporting data from local SQLite...
python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission --exclude=sessions --natural-foreign --natural-primary -o railway_data.json

echo.
echo Step 4: Setting DATABASE_URL and importing to Railway...
set DATABASE_URL=postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway
python manage.py loaddata railway_data.json

echo.
echo ============================================================
echo   TRANSFER COMPLETE!
echo ============================================================
echo.
pause

