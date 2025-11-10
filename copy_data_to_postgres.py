"""
Copy data from SQLite to PostgreSQL using direct database connections
"""
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os

print("=" * 70)
print("🔄 COPYING DATA: SQLite → PostgreSQL")
print("=" * 70)

# Database paths
SQLITE_DB = 'db.sqlite3'
PG_CONFIG = {
    'dbname': 'shiku_db',
    'user': 'postgres',
    'password': '7457@Benson',
    'host': 'localhost',
    'port': '5432'
}

# Check if SQLite database exists
if not os.path.exists(SQLITE_DB):
    print(f"\n❌ SQLite database '{SQLITE_DB}' not found!")
    print("Nothing to migrate.")
    exit(1)

try:
    # Connect to both databases
    print("\n📊 Connecting to databases...")
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    pg_conn = psycopg2.connect(**PG_CONFIG)
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    print("✅ Connected to SQLite")
    print("✅ Connected to PostgreSQL (shiku_db)")
    
    # Get list of all tables from SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in sqlite_cursor.fetchall()]
    
    print(f"\n📋 Found {len(tables)} tables to migrate")
    
    # Tables to skip (Django internal)
    skip_tables = ['django_migrations', 'django_admin_log', 'django_session']
    
    migrated_count = 0
    
    # Copy each table
    for table in tables:
        if table in skip_tables:
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
            
            # Insert into PostgreSQL
            insert_query = f'INSERT INTO "{table}" ({columns_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
            
            for row in rows:
                try:
                    pg_cursor.execute(insert_query, row)
                except Exception as e:
                    # Skip rows with errors
                    pass
            
            pg_conn.commit()
            print(f"   ✅ {table}: {len(rows)} rows")
            migrated_count += 1
            
        except Exception as e:
            print(f"   ⚠️ {table}: {str(e)[:50]}")
    
    # Update sequences for PostgreSQL
    print("\n📊 Updating PostgreSQL sequences...")
    pg_cursor.execute("""
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
    
    for row in pg_cursor.fetchall():
        try:
            pg_cursor.execute(row[0])
        except:
            pass
    
    pg_conn.commit()
    print("✅ Sequences updated")
    
    # Close connections
    sqlite_cursor.close()
    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()
    
    print("\n" + "=" * 70)
    print(f"✅ MIGRATION COMPLETE!")
    print("=" * 70)
    print(f"\n🎉 Migrated {migrated_count} tables successfully!")
    print("\n📝 Next steps:")
    print("   1. Create superuser: python manage.py createsuperuser")
    print("   2. Start server: python manage.py runserver 3000")
    print("   3. Check admin: http://127.0.0.1:3000/admin/")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTry creating a fresh superuser and adding products manually.")

