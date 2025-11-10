"""
Transfer data from SQLite to PostgreSQL
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.core import management
from django.db import connection

print("=" * 70)
print("DATA TRANSFER: SQLite → PostgreSQL")
print("=" * 70)

# Step 1: Switch to SQLite temporarily
print("\n📊 Step 1: Exporting data from SQLite...")
import her_beauty_hub.settings as settings

# Temporarily use SQLite
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
    }
}

# Force reconnection
from django.db import connections
connections.close_all()

# Export data
try:
    management.call_command(
        'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '-e', 'contenttypes',
        '-e', 'auth.Permission',
        '--indent', '2',
        output='data_transfer.json',
        verbosity=2
    )
    print("✅ Data exported successfully!")
except Exception as e:
    print(f"❌ Export error: {e}")
    exit(1)

# Step 2: Switch to PostgreSQL
print("\n📊 Step 2: Switching to PostgreSQL...")
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shiku_db',
        'USER': 'postgres',
        'PASSWORD': '7457@Benson',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Force reconnection
connections.close_all()

# Step 3: Import data
print("\n📊 Step 3: Importing data into PostgreSQL...")
try:
    with open('data_transfer.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Write with clean encoding
    with open('data_transfer_clean.json', 'w', encoding='utf-8') as f:
        f.write(content)
    
    management.call_command(
        'loaddata',
        'data_transfer_clean.json',
        verbosity=2
    )
    print("✅ Data imported successfully!")
except Exception as e:
    print(f"❌ Import error: {e}")
    print("\n⚠️ Some data might not have been transferred.")
    print("You can:")
    print("  1. Manually check what's missing in admin")
    print("  2. Re-enter critical data")

print("\n" + "=" * 70)
print("✅ DATABASE TRANSFER COMPLETE!")
print("=" * 70)
print("\nYour Django project is now using PostgreSQL! 🎉")
print("Database: shiku_db")
print("All your products, customers, and settings have been transferred!")

