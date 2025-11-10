"""
Add all products to Railway PostgreSQL from SQLite
"""
import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from beautyhub.models import HairStyle, Perfume, ClothingItem, GalleryItem, Video

print("=" * 70)
print("📦 ADDING PRODUCTS TO RAILWAY")
print("=" * 70)

# Connect to SQLite to read product data
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

print("\n✅ Reading products from SQLite...")

# Transfer Hairstyles
print("\n💇 Transferring Hairstyles...")
sqlite_cursor.execute("SELECT * FROM beautyhub_hairstyle")
hairstyle_rows = sqlite_cursor.fetchall()
sqlite_cursor.execute("PRAGMA table_info(beautyhub_hairstyle)")
columns = [col[1] for col in sqlite_cursor.fetchall()]

for row in hairstyle_rows:
    data = dict(zip(columns, row))
    try:
        HairStyle.objects.get_or_create(
            id=data['id'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'image': data['image'] or '',
                'price_ksh': data['price_ksh'],
                'price_usd': data.get('price_usd'),
                'price': data['price'],
                'duration_minutes': data['duration_minutes'],
                'duration': data['duration'],
                'difficulty': data['difficulty'],
                'available': data['available'],
                'featured': data['featured'],
            }
        )
        print(f"   ✅ {data['name']}")
    except Exception as e:
        print(f"   ⚠️ {data.get('name', 'Unknown')}: {str(e)[:50]}")

print(f"✅ Hairstyles: {HairStyle.objects.count()} total")

# Transfer Perfumes
print("\n🌸 Transferring Perfumes...")
sqlite_cursor.execute("SELECT * FROM beautyhub_perfume")
perfume_rows = sqlite_cursor.fetchall()
sqlite_cursor.execute("PRAGMA table_info(beautyhub_perfume)")
columns = [col[1] for col in sqlite_cursor.fetchall()]

for row in perfume_rows:
    data = dict(zip(columns, row))
    try:
        Perfume.objects.get_or_create(
            id=data['id'],
            defaults={
                'name': data['name'],
                'brand': data['brand'],
                'description': data['description'],
                'scent_type': data['scent_type'],
                'volume': data['volume'],
                'image': data['image'] or '',
                'price_ksh': data['price_ksh'],
                'price_usd': data.get('price_usd'),
                'price': data['price'],
                'stock_quantity': data['stock_quantity'],
                'available': data['available'],
                'featured': data['featured'],
            }
        )
        print(f"   ✅ {data['name']}")
    except Exception as e:
        print(f"   ⚠️ {data.get('name', 'Unknown')}: {str(e)[:50]}")

print(f"✅ Perfumes: {Perfume.objects.count()} total")

# Transfer Clothing
print("\n👗 Transferring Fashion...")
sqlite_cursor.execute("SELECT * FROM beautyhub_clothingitem")
clothing_rows = sqlite_cursor.fetchall()
sqlite_cursor.execute("PRAGMA table_info(beautyhub_clothingitem)")
columns = [col[1] for col in sqlite_cursor.fetchall()]

for row in clothing_rows:
    data = dict(zip(columns, row))
    try:
        ClothingItem.objects.get_or_create(
            id=data['id'],
            defaults={
                'name': data['name'],
                'category': data['category'],
                'description': data['description'],
                'available_sizes': data['available_sizes'],
                'image': data['image'] or '',
                'price_ksh': data['price_ksh'],
                'price_usd': data.get('price_usd'),
                'price': data['price'],
                'stock_quantity': data['stock_quantity'],
                'available': data['available'],
                'featured': data['featured'],
            }
        )
        print(f"   ✅ {data['name']}")
    except Exception as e:
        print(f"   ⚠️ {data.get('name', 'Unknown')}: {str(e)[:50]}")

print(f"✅ Clothing: {ClothingItem.objects.count()} total")

# Transfer Gallery Items
print("\n📸 Transferring Gallery...")
sqlite_cursor.execute("SELECT * FROM beautyhub_galleryitem")
gallery_rows = sqlite_cursor.fetchall()
sqlite_cursor.execute("PRAGMA table_info(beautyhub_galleryitem)")
columns = [col[1] for col in sqlite_cursor.fetchall()]

for row in gallery_rows:
    data = dict(zip(columns, row))
    try:
        GalleryItem.objects.get_or_create(
            id=data['id'],
            defaults={
                'title': data['title'],
                'description': data['description'],
                'category': data['category'],
                'image': data['image'] or '',
                'featured': data['featured'],
            }
        )
        print(f"   ✅ {data['title']}")
    except Exception as e:
        print(f"   ⚠️ {data.get('title', 'Unknown')}: {str(e)[:50]}")

print(f"✅ Gallery: {GalleryItem.objects.count()} total")

# Transfer Videos
print("\n🎥 Transferring Videos...")
sqlite_cursor.execute("SELECT * FROM beautyhub_video")
video_rows = sqlite_cursor.fetchall()
sqlite_cursor.execute("PRAGMA table_info(beautyhub_video)")
columns = [col[1] for col in sqlite_cursor.fetchall()]

for row in video_rows:
    data = dict(zip(columns, row))
    try:
        Video.objects.get_or_create(
            id=data['id'],
            defaults={
                'title': data['title'],
                'description': data['description'],
                'category': data['category'],
                'video_file': data['video_file'] or '',
                'thumbnail': data['thumbnail'] or '',
                'duration': data['duration'],
                'featured': data['featured'],
                'active': data['active'],
                'views': data['views'],
            }
        )
        print(f"   ✅ {data['title']}")
    except Exception as e:
        print(f"   ⚠️ {data.get('title', 'Unknown')}: {str(e)[:50]}")

print(f"✅ Videos: {Video.objects.count()} total")

# Close SQLite connection
sqlite_cursor.close()
sqlite_conn.close()

# Final count
print("\n" + "=" * 70)
print("✅ PRODUCTS ADDED TO RAILWAY!")
print("=" * 70)
print(f"\n📊 Final Count:")
print(f"   💇 Hairstyles: {HairStyle.objects.count()}")
print(f"   🌸 Perfumes: {Perfume.objects.count()}")
print(f"   👗 Clothing: {ClothingItem.objects.count()}")
print(f"   📸 Gallery: {GalleryItem.objects.count()}")
print(f"   🎥 Videos: {Video.objects.count()}")
print(f"   📦 Orders: {OrderMessage.objects.count()}")
print(f"\n🎉 Total: {HairStyle.objects.count() + Perfume.objects.count() + ClothingItem.objects.count() + GalleryItem.objects.count() + Video.objects.count()} products")
print("\n🚂 Your Shiku Beauty Hub is ready on Railway!")
print("\n✨ Admin Login:")
print("   Username: admin")
print("   Password: shiku2025")

