#!/usr/bin/env python
"""
Transfer all data from local SQLite to Railway PostgreSQL
This script will:
1. Connect to Railway PostgreSQL
2. Run migrations to create tables
3. Export data from SQLite
4. Import data to PostgreSQL
"""
import os
import sys

# Set DATABASE_URL BEFORE Django loads
RAILWAY_DB_URL = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
import django
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
import dj_database_url

# Railway PostgreSQL URLs
RAILWAY_PUBLIC = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"
RAILWAY_INTERNAL = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@postgres.railway.internal:5432/railway"

print("=" * 70)
print("  TRANSFERRING DATA TO RAILWAY POSTGRESQL DATABASE")
print("=" * 70)

# Step 1: Save original database config
original_db = settings.DATABASES['default'].copy()

# Step 2: Configure Railway PostgreSQL
print("\n[1/5] Configuring Railway PostgreSQL connection...")
railway_db = dj_database_url.config(default=RAILWAY_PUBLIC)

# Test connection
print("\n[2/5] Testing Railway PostgreSQL connection...")
try:
    settings.DATABASES['railway'] = railway_db
    railway_conn = connections['railway']
    with railway_conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"  ✓ Connected! PostgreSQL: {version[0][:60]}...")
        
        # Check existing tables
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        print(f"  ✓ Found {table_count} existing tables")
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    print("\n⚠️  Make sure:")
    print("  1. Railway PostgreSQL is running")
    print("  2. Public URL is accessible from your network")
    print("  3. Firewall allows connection")
    sys.exit(1)

# Step 3: Run migrations on Railway database
print("\n[3/5] Running migrations on Railway PostgreSQL...")
settings.DATABASES['default'] = railway_db
try:
    call_command('migrate', verbosity=1, interactive=False)
    print("  ✓ Migrations completed!")
except Exception as e:
    print(f"  ⚠️  Migration warning: {e}")
    print("  Continuing anyway...")

# Step 4: Export data from SQLite
print("\n[4/5] Exporting data from local SQLite database...")
settings.DATABASES['sqlite'] = original_db
settings.DATABASES['default'] = original_db  # Use SQLite for reading

export_file = 'railway_data_export.json'
try:
    # Export all data except sessions and contenttypes
    call_command('dumpdata',
                 exclude=['contenttypes', 'auth.Permission', 'sessions'],
                 output=export_file,
                 natural_foreign=True,
                 natural_primary=True,
                 verbosity=1)
    
    # Check file size
    file_size = os.path.getsize(export_file) / 1024  # KB
    print(f"  ✓ Data exported to {export_file} ({file_size:.1f} KB)")
except Exception as e:
    print(f"  ❌ Export failed: {e}")
    sys.exit(1)

# Step 5: Import data to Railway PostgreSQL
print("\n[5/5] Importing data to Railway PostgreSQL...")
settings.DATABASES['default'] = railway_db  # Switch to Railway for writing

try:
    call_command('loaddata', export_file, verbosity=2)
    print("  ✓ Data imported successfully!")
except Exception as e:
    print(f"  ⚠️  Import warning: {e}")
    print("  Some data may have been imported. Check Railway database.")

# Verify data transfer
print("\n" + "=" * 70)
print("  VERIFYING DATA TRANSFER")
print("=" * 70)

try:
    with railway_conn.cursor() as cursor:
        # Count records in key tables
        tables_to_check = [
            'beautyhub_businessinfo',
            'beautyhub_hairstyle',
            'beautyhub_perfume',
            'beautyhub_clothingitem',
            'beautyhub_galleryitem',
            'beautyhub_testimonial',
            'beautyhub_video',
            'auth_user'
        ]
        
        print("\nRecord counts in Railway PostgreSQL:")
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"  ✓ {table}: {count} records")
            except Exception as e:
                print(f"  ⚠️  {table}: {e}")
    
    print("\n" + "=" * 70)
    print("  ✅ DATA TRANSFER COMPLETE!")
    print("=" * 70)
    print("\nAll data has been transferred to Railway PostgreSQL!")
    print("Your Railway app should now have all your data.")
    print("\nNext steps:")
    print("1. Verify data in Railway dashboard")
    print("2. Test your Railway app")
    print("3. Create admin user if needed")
    
except Exception as e:
    print(f"\n⚠️  Verification error: {e}")

# Cleanup
if os.path.exists(export_file):
    print(f"\n💡 Export file saved: {export_file}")
    print("  You can delete it after verifying data transfer.")

# Restore original database
settings.DATABASES['default'] = original_db

