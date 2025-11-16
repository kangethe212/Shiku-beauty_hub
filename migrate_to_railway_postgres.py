#!/usr/bin/env python
"""
Script to migrate data from SQLite to Railway PostgreSQL
Run this locally to transfer all data to Railway database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings

# Railway PostgreSQL connection string (Public URL for local connection)
RAILWAY_DB_URL = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"

print("=" * 60)
print("MIGRATING DATA TO RAILWAY POSTGRESQL")
print("=" * 60)

# Configure database connection
import dj_database_url
railway_db = dj_database_url.config(default=RAILWAY_DB_URL)

print(f"\n✓ Connecting to Railway PostgreSQL...")
print(f"  Host: yamanote.proxy.rlwy.net")
print(f"  Port: 27057")
print(f"  Database: railway")

# Temporarily set Railway database
original_db = settings.DATABASES['default']
settings.DATABASES['railway'] = railway_db

try:
    # Test connection
    print("\n✓ Testing connection...")
    railway_conn = connections['railway']
    with railway_conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"  PostgreSQL version: {version[0][:50]}...")
    
    print("\n✓ Connection successful!")
    
    # Run migrations on Railway database
    print("\n" + "=" * 60)
    print("RUNNING MIGRATIONS ON RAILWAY DATABASE")
    print("=" * 60)
    
    # Set Railway as default temporarily
    settings.DATABASES['default'] = railway_db
    
    # Run migrations
    call_command('migrate', verbosity=2, database='default')
    
    print("\n✓ Migrations completed!")
    
    # Now transfer data from SQLite to PostgreSQL
    print("\n" + "=" * 60)
    print("TRANSFERRING DATA FROM SQLITE TO POSTGRESQL")
    print("=" * 60)
    
    # Switch back to SQLite for reading
    settings.DATABASES['sqlite'] = original_db
    settings.DATABASES['default'] = railway_db
    
    # Use dumpdata and loaddata
    print("\n✓ Exporting data from SQLite...")
    call_command('dumpdata', 
                 exclude=['contenttypes', 'auth.Permission', 'sessions'],
                 output='data_export.json',
                 database='sqlite',
                 natural_foreign=True,
                 natural_primary=True)
    
    print("✓ Data exported to data_export.json")
    
    print("\n✓ Importing data to Railway PostgreSQL...")
    call_command('loaddata', 'data_export.json', database='default', verbosity=2)
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print("\nAll data has been transferred to Railway PostgreSQL!")
    print("Your Railway app should now have all your data.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n⚠️  Migration failed. Check the error above.")
finally:
    # Restore original database
    settings.DATABASES['default'] = original_db

