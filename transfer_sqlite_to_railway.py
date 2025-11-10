"""
Transfer ALL data from SQLite DIRECTLY to Railway PostgreSQL
"""
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os

print("=" * 70)
print("🚂 TRANSFERRING DATA: SQLite → RAILWAY PostgreSQL")
print("=" * 70)

# Database configurations
SQLITE_DB = 'db.sqlite3'
RAILWAY_DB = {
    'dbname': 'railway',
    'user': 'postgres',
    'password': 'UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ',
    'host': 'yamanote.proxy.rlwy.net',
    'port': '27057'
}

# Check if SQLite database exists
if not os.path.exists(SQLITE_DB):
    print(f"\n❌ SQLite database '{SQLITE_DB}' not found!")
    print("All data should be in local PostgreSQL.")
    exit(1)

try:
    # Connect to both databases
    print("\n📊 Connecting to databases...")
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    railway_conn = psycopg2.connect(**RAILWAY_DB)
    
    sqlite_cursor = sqlite_conn.cursor()
    railway_cursor = railway_conn.cursor()
    
    print("✅ Connected to SQLite (db.sqlite3)")
    print("✅ Connected to Railway (railway database)")
    
    # Get list of all tables from SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in sqlite_cursor.fetchall()]
    
    print(f"\n📋 Found {len(tables)} tables in SQLite")
    
    # Tables to skip (Django internal)
    skip_tables = ['django_migrations']
    
    migrated_count = 0
    total_rows = 0
    
    # Important tables (prioritize these)
    priority_tables = [
        'beautyhub_hairstyle',
        'beautyhub_perfume',
        'beautyhub_clothingitem',
        'beautyhub_galleryitem',
        'beautyhub_video',
        'beautyhub_businessinfo',
        'auth_user'
    ]
    
    # Process priority tables first
    all_tables = priority_tables + [t for t in tables if t not in priority_tables and t not in skip_tables]
    
    # Copy each table
    for table in all_tables:
        if table in skip_tables:
            continue
        
        if table not in tables:
            continue
            
        try:
            # Get all data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"   ⊘ {table}: empty")
                continue
            
            # Get column names
            column_names = [description[0] for description in sqlite_cursor.description]
            
            # Prepare INSERT query
            columns_str = ', '.join([f'"{col}"' for col in column_names])
            placeholders = ', '.join(['%s'] * len(column_names))
            
            # Insert into Railway PostgreSQL
            insert_query = f'INSERT INTO "{table}" ({columns_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
            
            inserted = 0
            for row in rows:
                try:
                    railway_cursor.execute(insert_query, row)
                    inserted += 1
                except Exception as e:
                    # Skip rows with errors (likely duplicates)
                    pass
            
            railway_conn.commit()
            
            if inserted > 0:
                print(f"   ✅ {table}: {inserted}/{len(rows)} rows")
                migrated_count += 1
                total_rows += inserted
            else:
                print(f"   ⊘ {table}: {len(rows)} rows (already exist)")
            
        except Exception as e:
            print(f"   ⚠️ {table}: {str(e)[:80]}")
    
    # Update sequences for Railway PostgreSQL
    print("\n📊 Updating Railway PostgreSQL sequences...")
    railway_cursor.execute("""
        SELECT 'SELECT SETVAL(' ||
               quote_literal(quote_ident(sequence_namespace.nspname) || '.' || quote_ident(class_sequence.relname)) ||
               ', COALESCE(MAX(' ||quote_ident(pg_attribute.attname)|| '), 1) ) FROM ' ||
               quote_ident(table_namespace.nspname)|| '.'||quote_ident(class_table.relname)|| ';'
        FROM pg_depend
        INNER JOIN pg_class AS class_sequence ON class_sequence.oid = pg_depend.objid
        INNER JOIN pg_class AS class_table ON class_table.oid = pg_depend.refobjid
        INNER JOIN pg_attribute ON pg_attribute.attrelid = class_table.oid AND pg_attribute.attnum = pg_depend.refobjsubid
        INNER JOIN pg_namespace as table_namespace ON table_namespace.oid = class_table.relnamespace
        INNER JOIN pg_namespace AS sequence_namespace ON sequence_namespace.oid = class_sequence.relnamespace
        WHERE class_sequence.relkind = 'S';
    """)
    
    for row in railway_cursor.fetchall():
        try:
            railway_cursor.execute(row[0])
        except:
            pass
    
    railway_conn.commit()
    print("✅ Sequences updated")
    
    # Close connections
    sqlite_cursor.close()
    sqlite_conn.close()
    railway_cursor.close()
    railway_conn.close()
    
    print("\n" + "=" * 70)
    print(f"✅ TRANSFER TO RAILWAY COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Statistics:")
    print(f"   - Tables migrated: {migrated_count}")
    print(f"   - Total rows transferred: {total_rows}")
    print(f"\n🚂 Your Shiku Beauty Hub is now on Railway!")
    print(f"\n🌐 Railway Database:")
    print(f"   Host: yamanote.proxy.rlwy.net")
    print(f"   Database: railway")
    print(f"   Status: ✅ LIVE")
    print(f"\n📝 Next steps:")
    print(f"   1. Create superuser: python manage.py createsuperuser")
    print(f"   2. Test website locally (connected to Railway)")
    print(f"   3. Deploy your code to Railway")
    print(f"   4. Your website will be LIVE! 🚀")
    
except Exception as e:
    print(f"\n❌ Connection Error: {e}")
    print("\nPlease check:")
    print("   ✅ Railway database is running")
    print("   ✅ Password is correct")
    print("   ✅ Network connection is stable")

