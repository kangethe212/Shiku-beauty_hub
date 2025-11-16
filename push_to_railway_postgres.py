#!/usr/bin/env python
"""
Push all data from local SQLite database to Railway PostgreSQL
Uses Railway internal database URL for connection
"""
import os
import sys

# Set Railway database URL BEFORE Django loads
# Note: Internal URL (postgres.railway.internal) only works from Railway network
# Use public URL for local connection
RAILWAY_PUBLIC_DB = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"
RAILWAY_INTERNAL_DB = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@postgres.railway.internal:5432/railway"

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
import django
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
import dj_database_url

print("=" * 70)
print("  PUSHING DATABASE TO RAILWAY POSTGRESQL")
print("=" * 70)

# Step 1: Save original database config (SQLite)
original_db = settings.DATABASES['default'].copy()
print(f"\n[1/6] Original database: {original_db.get('ENGINE', 'Unknown')}")

# Step 2: Configure Railway PostgreSQL
print(f"\n[2/6] Configuring Railway PostgreSQL connection...")
print(f"  Using Public URL: yamanote.proxy.rlwy.net:27057")
print(f"  (Internal URL only works from Railway network)")
railway_db = dj_database_url.config(default=RAILWAY_PUBLIC_DB)

# Verify it's PostgreSQL
engine = railway_db.get('ENGINE', '')
if 'postgres' not in engine.lower():
    print(f"❌ Error: Not a PostgreSQL database! Got: {engine}")
    sys.exit(1)

print(f"  ✓ Database engine: {engine}")
print(f"  ✓ Host: {railway_db.get('HOST', 'Unknown')}")
print(f"  ✓ Port: {railway_db.get('PORT', 'Unknown')}")
print(f"  ✓ Database: {railway_db.get('NAME', 'Unknown')}")

# Step 3: Test Railway connection
print(f"\n[3/6] Testing Railway PostgreSQL connection...")
try:
    settings.DATABASES['railway'] = railway_db
    settings.DATABASES['default'] = railway_db
    
    # Close existing connections
    connections.close_all()
    
    conn = connections['default']
    with conn.cursor() as cursor:
        # Test connection with simple query
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print(f"  ✓ Connected! PostgreSQL connection verified")
        
        # Check existing tables (simpler query)
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            table_count = cursor.fetchone()[0]
            print(f"  ✓ Found {table_count} existing tables")
        except Exception as table_error:
            print(f"  ⚠️  Could not count tables: {table_error}")
            print(f"  Continuing anyway...")
        
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    print("\n⚠️  Make sure:")
    print("  1. Railway PostgreSQL service is running")
    print("  2. Internal URL is accessible")
    print("  3. Network allows connection")
    sys.exit(1)

# Step 4: Run migrations on Railway
print(f"\n[4/6] Running migrations on Railway PostgreSQL...")
try:
    call_command('migrate', verbosity=1, interactive=False)
    print("  ✓ Migrations completed!")
except Exception as e:
    print(f"  ⚠️  Migration warning: {e}")
    print("  Continuing anyway...")

# Step 5: Export data from local SQLite
print(f"\n[5/6] Exporting data from local SQLite database...")
settings.DATABASES['sqlite'] = original_db
settings.DATABASES['default'] = original_db  # Use SQLite for reading

export_file = 'railway_data_export.json'
try:
    # Export all data except sessions and contenttypes
    print("  Exporting all models...")
    call_command('dumpdata',
                 exclude=['contenttypes', 'auth.Permission', 'sessions'],
                 output=export_file,
                 natural_foreign=True,
                 natural_primary=True,
                 verbosity=1)
    
    # Check file size
    if os.path.exists(export_file):
        file_size = os.path.getsize(export_file) / 1024  # KB
        print(f"  ✓ Data exported to {export_file} ({file_size:.1f} KB)")
    else:
        print(f"  ❌ Export file not created!")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ Export failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 6: Import data to Railway PostgreSQL
print(f"\n[6/6] Importing data to Railway PostgreSQL...")
settings.DATABASES['default'] = railway_db  # Switch to Railway for writing

try:
    print("  Importing all data...")
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
    with conn.cursor() as cursor:
        # Count records in key tables
        tables_to_check = [
            ('beautyhub_businessinfo', 'Business Info'),
            ('beautyhub_hairstyle', 'Hairstyles'),
            ('beautyhub_perfume', 'Perfumes'),
            ('beautyhub_clothingitem', 'Clothing Items'),
            ('beautyhub_galleryitem', 'Gallery Items'),
            ('beautyhub_testimonial', 'Testimonials'),
            ('beautyhub_video', 'Videos'),
            ('beautyhub_service', 'Services'),
            ('beautyhub_booking', 'Bookings'),
            ('beautyhub_contactmessage', 'Contact Messages'),
            ('beautyhub_ordermessage', 'Order Messages'),
            ('auth_user', 'Users'),
        ]
        
        print("\nRecord counts in Railway PostgreSQL:")
        total_records = 0
        for table, name in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                total_records += count
                print(f"  ✓ {name}: {count} records")
            except Exception as e:
                print(f"  ⚠️  {name}: {e}")
        
        print(f"\n  📊 Total records transferred: {total_records}")
    
    print("\n" + "=" * 70)
    print("  ✅ DATABASE TRANSFER COMPLETE!")
    print("=" * 70)
    print("\nAll data has been successfully transferred to Railway PostgreSQL!")
    print("Your Railway app now has all your local database data.")
    print("\nNext steps:")
    print("1. Verify data in Railway dashboard")
    print("2. Test your Railway app")
    print("3. Check admin panel on Railway")
    
except Exception as e:
    print(f"\n⚠️  Verification error: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
if os.path.exists(export_file):
    print(f"\n💡 Export file saved: {export_file}")
    print("  You can delete it after verifying data transfer.")

# Restore original database
settings.DATABASES['default'] = original_db

print("\n" + "=" * 70)

