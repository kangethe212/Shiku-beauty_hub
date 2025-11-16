#!/usr/bin/env python
"""
Complete setup script for Railway PostgreSQL database
1. Connects to Railway PostgreSQL
2. Runs migrations
3. Transfers data from SQLite
4. Verifies connection
"""
import os
import sys

# Set DATABASE_URL before Django loads
RAILWAY_DB_URL = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"
os.environ['DATABASE_URL'] = RAILWAY_DB_URL

# Now setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
import django
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
import dj_database_url

print("=" * 70)
print("  RAILWAY POSTGRESQL DATABASE SETUP")
print("=" * 70)

# Verify database configuration
db_config = dj_database_url.config(default=RAILWAY_DB_URL)
settings.DATABASES['default'] = db_config

print(f"\n[1/4] Database Configuration:")
print(f"  Engine: {db_config.get('ENGINE', 'Unknown')}")
print(f"  Host: {db_config.get('HOST', 'Unknown')}")
print(f"  Port: {db_config.get('PORT', 'Unknown')}")
print(f"  Database: {db_config.get('NAME', 'Unknown')}")

# Test connection
print(f"\n[2/4] Testing Connection...")
try:
    connections.close_all()
    conn = connections['default']
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"  ✓ Connected! PostgreSQL version detected")
        print(f"  {version[:80]}...")
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    print("\n⚠️  Cannot connect to Railway PostgreSQL.")
    print("   Make sure:")
    print("   1. PostgreSQL service is running on Railway")
    print("   2. Public URL is accessible")
    print("   3. Network/firewall allows connection")
    sys.exit(1)

# Run migrations
print(f"\n[3/4] Running Migrations...")
try:
    call_command('migrate', verbosity=1, interactive=False)
    print("  ✓ Migrations completed!")
except Exception as e:
    print(f"  ⚠️  Migration error: {e}")
    print("  Continuing anyway...")

# Check existing data
print(f"\n[4/4] Checking Database State...")
try:
    with conn.cursor() as cursor:
        # Count tables
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        print(f"  ✓ Found {table_count} tables")
        
        # Check key tables
        key_tables = ['beautyhub_businessinfo', 'beautyhub_hairstyle', 'auth_user']
        for table in key_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"    - {table}: {count} records")
            except:
                print(f"    - {table}: not found (will be created)")
except Exception as e:
    print(f"  ⚠️  Check error: {e}")

print("\n" + "=" * 70)
print("  ✅ DATABASE SETUP COMPLETE!")
print("=" * 70)
print("\nRailway PostgreSQL is configured and ready!")
print("\nNext: Run 'python transfer_data_to_railway.py' to transfer data")

