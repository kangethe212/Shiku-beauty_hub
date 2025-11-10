"""
Transfer data from LOCAL PostgreSQL to RAILWAY PostgreSQL
"""
import psycopg2
from psycopg2.extras import execute_values

print("=" * 70)
print("🚂 TRANSFERRING DATA TO RAILWAY")
print("=" * 70)

# Database configurations
LOCAL_DB = {
    'dbname': 'shiku_db',
    'user': 'postgres',
    'password': '7457@Benson',
    'host': 'localhost',
    'port': '5432'
}

RAILWAY_DB = {
    'dbname': 'railway',
    'user': 'postgres',
    'password': 'UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ',
    'host': 'yamanote.proxy.rlwy.net',
    'port': '27057'
}

try:
    # Connect to both databases
    print("\n📊 Connecting to databases...")
    local_conn = psycopg2.connect(**LOCAL_DB)
    railway_conn = psycopg2.connect(**RAILWAY_DB)
    
    local_cursor = local_conn.cursor()
    railway_cursor = railway_conn.cursor()
    
    print("✅ Connected to LOCAL database (shiku_db)")
    print("✅ Connected to RAILWAY database (railway)")
    
    # Get list of all tables
    local_cursor.execute("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename NOT LIKE 'django_migrations'
    """)
    tables = [row[0] for row in local_cursor.fetchall()]
    
    print(f"\n📋 Found {len(tables)} tables to migrate")
    
    migrated_count = 0
    total_rows = 0
    
    # Copy each table
    for table in tables:
        try:
            # Get all data from local
            local_cursor.execute(f'SELECT * FROM "{table}"')
            rows = local_cursor.fetchall()
            
            if not rows:
                print(f"   ⊘ {table}: empty")
                continue
            
            # Get column names
            column_names = [desc[0] for desc in local_cursor.description]
            columns_str = ', '.join([f'"{col}"' for col in column_names])
            placeholders = ', '.join(['%s'] * len(column_names))
            
            # Insert into Railway
            insert_query = f'INSERT INTO "{table}" ({columns_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
            
            inserted = 0
            for row in rows:
                try:
                    railway_cursor.execute(insert_query, row)
                    inserted += 1
                except Exception as e:
                    # Skip rows with errors
                    pass
            
            railway_conn.commit()
            print(f"   ✅ {table}: {inserted}/{len(rows)} rows")
            migrated_count += 1
            total_rows += inserted
            
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
    local_cursor.close()
    local_conn.close()
    railway_cursor.close()
    railway_conn.close()
    
    print("\n" + "=" * 70)
    print(f"✅ TRANSFER TO RAILWAY COMPLETE!")
    print("=" * 70)
    print(f"\n🎉 Statistics:")
    print(f"   - Tables migrated: {migrated_count}")
    print(f"   - Total rows: {total_rows}")
    print(f"\n🚂 Your data is now on Railway!")
    print(f"   Host: yamanote.proxy.rlwy.net")
    print(f"   Database: railway")
    print(f"\n📝 Next steps:")
    print(f"   1. Create superuser: python manage.py createsuperuser")
    print(f"   2. Test your website")
    print(f"   3. Deploy to Railway!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nConnection details:")
    print(f"   Local: {LOCAL_DB['host']}:{LOCAL_DB['port']}/{LOCAL_DB['dbname']}")
    print(f"   Railway: {RAILWAY_DB['host']}:{RAILWAY_DB['port']}/{RAILWAY_DB['dbname']}")
    print("\nMake sure:")
    print("   ✅ PostgreSQL is running locally")
    print("   ✅ Railway database is accessible")
    print("   ✅ Password is correct")

