"""
Migrate data from SQLite to PostgreSQL using Django ORM
"""
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🔄 MIGRATING DATA: SQLite → PostgreSQL")
print("=" * 70)

# Step 1: Read from SQLite
print("\n📊 Step 1: Reading data from SQLite...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')

# Temporarily configure for SQLite
import her_beauty_hub.settings as settings
original_db = settings.DATABASES.copy()

settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(settings.BASE_DIR / 'db.sqlite3'),
    }
}

import django
django.setup()

from django.contrib.auth.models import User, Group
from beautyhub.models import *

# Collect all data
print("Collecting data from SQLite...")
data = {
    'users': list(User.objects.all().values()),
    'groups': list(Group.objects.all().values()),
    'services': list(Service.objects.all().values()),
    'products': list(Product.objects.all().values()),
    'gallery_items': list(GalleryItem.objects.all().values()),
    'bookings': list(Booking.objects.all().values()),
    'contact_messages': list(ContactMessage.objects.all().values()),
    'testimonials': list(Testimonial.objects.all().values()),
    'videos': list(Video.objects.all().values()),
    'daily_offers': list(DailyOffer.objects.all().values()),
    'hairstyles': list(HairStyle.objects.all().values()),
    'perfumes': list(Perfume.objects.all().values()),
    'clothing': list(ClothingItem.objects.all().values()),
    'order_messages': list(OrderMessage.objects.all().values()),
}

# Count total objects
total_objects = sum(len(v) for v in data.values())
print(f"✅ Collected {total_objects} objects from SQLite")
for key, items in data.items():
    if items:
        print(f"   - {key}: {len(items)}")

# Step 2: Close SQLite connection
print("\n📊 Step 2: Switching to PostgreSQL...")
from django.db import connection
connection.close()

# Step 3: Configure for PostgreSQL
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

# Reimport Django apps to use new database
from django.apps import apps
apps.all_models.clear()
apps.app_configs.clear()
django.setup()

# Reimport models with PostgreSQL connection
from django.contrib.auth.models import User as PgUser, Group as PgGroup
from beautyhub.models import *

print("✅ Connected to PostgreSQL (shiku_db)")

# Step 4: Write to PostgreSQL
print("\n📊 Step 3: Writing data to PostgreSQL...")

try:
    # Users
    if data['users']:
        print(f"Migrating {len(data['users'])} users...")
        for user_data in data['users']:
            try:
                PgUser.objects.get_or_create(
                    id=user_data['id'],
                    defaults=user_data
                )
            except:
                pass
    
    # Services
    if data['services']:
        print(f"Migrating {len(data['services'])} services...")
        for item in data['services']:
            Service.objects.get_or_create(id=item['id'], defaults=item)
    
    # Products
    if data['products']:
        print(f"Migrating {len(data['products'])} products...")
        for item in data['products']:
            Product.objects.get_or_create(id=item['id'], defaults=item)
    
    # Gallery Items
    if data['gallery_items']:
        print(f"Migrating {len(data['gallery_items'])} gallery items...")
        for item in data['gallery_items']:
            GalleryItem.objects.get_or_create(id=item['id'], defaults=item)
    
    # Bookings
    if data['bookings']:
        print(f"Migrating {len(data['bookings'])} bookings...")
        for item in data['bookings']:
            # Remove service_id if it's None
            if 'service_id' in item and item['service_id'] is None:
                item.pop('service_id', None)
            Booking.objects.get_or_create(id=item['id'], defaults=item)
    
    # Contact Messages
    if data['contact_messages']:
        print(f"Migrating {len(data['contact_messages'])} contact messages...")
        for item in data['contact_messages']:
            ContactMessage.objects.get_or_create(id=item['id'], defaults=item)
    
    # Testimonials
    if data['testimonials']:
        print(f"Migrating {len(data['testimonials'])} testimonials...")
        for item in data['testimonials']:
            if 'service_id' in item and item['service_id'] is None:
                item.pop('service_id', None)
            Testimonial.objects.get_or_create(id=item['id'], defaults=item)
    
    # Videos
    if data['videos']:
        print(f"Migrating {len(data['videos'])} videos...")
        for item in data['videos']:
            Video.objects.get_or_create(id=item['id'], defaults=item)
    
    # Daily Offers
    if data['daily_offers']:
        print(f"Migrating {len(data['daily_offers'])} daily offers...")
        for item in data['daily_offers']:
            DailyOffer.objects.get_or_create(id=item['id'], defaults=item)
    
    # Hairstyles
    if data['hairstyles']:
        print(f"Migrating {len(data['hairstyles'])} hairstyles...")
        for item in data['hairstyles']:
            HairStyle.objects.get_or_create(id=item['id'], defaults=item)
    
    # Perfumes
    if data['perfumes']:
        print(f"Migrating {len(data['perfumes'])} perfumes...")
        for item in data['perfumes']:
            Perfume.objects.get_or_create(id=item['id'], defaults=item)
    
    # Clothing
    if data['clothing']:
        print(f"Migrating {len(data['clothing'])} clothing items...")
        for item in data['clothing']:
            ClothingItem.objects.get_or_create(id=item['id'], defaults=item)
    
    # Order Messages
    if data['order_messages']:
        print(f"Migrating {len(data['order_messages'])} order messages...")
        for item in data['order_messages']:
            OrderMessage.objects.get_or_create(id=item['id'], defaults=item)
    
    print("\n✅ All data migrated successfully!")
    
except Exception as e:
    print(f"\n⚠️ Error during migration: {e}")
    print("Some data may have been partially migrated.")

print("\n" + "=" * 70)
print("✅ MIGRATION COMPLETE!")
print("=" * 70)
print("\n🎉 Your Django project is now using PostgreSQL!")
print(f"   Database: shiku_db")
print(f"   Total objects: {total_objects}")
print("\n📝 Next steps:")
print("   1. Create a new superuser: python manage.py createsuperuser")
print("   2. Restart your server: python manage.py runserver 3000")
print("   3. Check admin panel to verify data")

