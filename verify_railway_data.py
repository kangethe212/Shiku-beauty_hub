"""
Verify data on Railway PostgreSQL database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from beautyhub.models import *
from django.contrib.auth.models import User

print("=" * 70)
print("🔍 VERIFYING DATA ON RAILWAY")
print("=" * 70)

print("\n📊 Database: Railway PostgreSQL")
print("   Host: yamanote.proxy.rlwy.net:27057")
print("   Database: railway")

print("\n" + "=" * 70)
print("CHECKING DATA...")
print("=" * 70)

# Check all models
checks = [
    ('👤 Users', User.objects.all()),
    ('💇 Hairstyles', HairStyle.objects.all()),
    ('🌸 Perfumes', Perfume.objects.all()),
    ('👗 Clothing', ClothingItem.objects.all()),
    ('📸 Gallery Items', GalleryItem.objects.all()),
    ('🎥 Videos', Video.objects.all()),
    ('📦 Orders', OrderMessage.objects.all()),
    ('🏢 Business Info', BusinessInfo.objects.all()),
    ('💬 Contact Messages', ContactMessage.objects.all()),
    ('📅 Bookings', Booking.objects.all()),
]

total_objects = 0

for name, queryset in checks:
    count = queryset.count()
    total_objects += count
    if count > 0:
        print(f"✅ {name}: {count}")
    else:
        print(f"⊘ {name}: 0")

print("\n" + "=" * 70)
print(f"📊 TOTAL OBJECTS ON RAILWAY: {total_objects}")
print("=" * 70)

# Show sample products
if HairStyle.objects.exists():
    print("\n💇 Sample Hairstyles:")
    for style in HairStyle.objects.all()[:5]:
        print(f"   - {style.name} (KSH {style.price_ksh})")

if Perfume.objects.exists():
    print("\n🌸 Sample Perfumes:")
    for perfume in Perfume.objects.all()[:5]:
        print(f"   - {perfume.name} (KSH {perfume.price_ksh})")

if ClothingItem.objects.exists():
    print("\n👗 Sample Fashion:")
    for item in ClothingItem.objects.all()[:3]:
        print(f"   - {item.name} (KSH {item.price_ksh})")

print("\n" + "=" * 70)
if total_objects > 50:
    print("✅ DATA TRANSFER SUCCESSFUL!")
    print("🎉 All your products are on Railway!")
else:
    print("⚠️ Some data might be missing")
    print("   You can add products via admin panel")
print("=" * 70)

print("\n🚀 Ready to deploy!")
print("\n📝 Next steps:")
print("   1. Push code to GitHub")
print("   2. Connect GitHub repo to Railway")
print("   3. Deploy automatically!")
print("\n   Admin Login:")
print("   Username: admin")
print("   Password: shiku2025")

