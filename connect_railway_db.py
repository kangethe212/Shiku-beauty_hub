#!/usr/bin/env python
"""
Quick script to test Railway PostgreSQL connection and run migrations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
import dj_database_url

# Railway PostgreSQL URLs
RAILWAY_INTERNAL = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@postgres.railway.internal:5432/railway"
RAILWAY_PUBLIC = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"

# Note: Use PUBLIC URL from local machine, INTERNAL URL from Railway

print("=" * 60)
print("CONNECTING TO RAILWAY POSTGRESQL")
print("=" * 60)

# Try public URL first (works from local machine)
db_url = RAILWAY_PUBLIC
print(f"\nUsing Public URL: yamanote.proxy.rlwy.net:27057")

# Configure database
railway_db = dj_database_url.config(default=db_url)

# Set as default database BEFORE any Django operations
settings.DATABASES['default'] = railway_db

# Close any existing connections
connections.close_all()

try:
    # Test connection
    print("\n✓ Testing connection...")
    conn = connections['default']
    
    # Verify it's PostgreSQL
    engine = settings.DATABASES['default'].get('ENGINE', '')
    print(f"  Database engine: {engine}")
    
    if 'postgres' not in engine.lower():
        raise ValueError(f"Not PostgreSQL! Using: {engine}")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"  ✓ Connected! PostgreSQL: {version[0][:50]}...")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\n  ✓ Found {len(tables)} tables in database")
        
        if tables:
            print("  Tables:")
            for table in tables[:10]:  # Show first 10
                print(f"    - {table[0]}")
            if len(tables) > 10:
                print(f"    ... and {len(tables) - 10} more")
    
    # Run migrations
    print("\n" + "=" * 60)
    print("RUNNING MIGRATIONS")
    print("=" * 60)
    call_command('migrate', verbosity=2)
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print("\nRailway PostgreSQL is connected and migrations are complete!")
    print("Your database is ready to use.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n⚠️  Connection failed. Check:")
    print("  1. Database URL is correct")
    print("  2. Network allows connection to Railway")
    print("  3. PostgreSQL service is running on Railway")

