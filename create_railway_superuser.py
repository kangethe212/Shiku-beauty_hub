"""
Create superuser on Railway PostgreSQL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 70)
print("👤 CREATING SUPERUSER ON RAILWAY")
print("=" * 70)

# Create superuser
try:
    if User.objects.filter(username='admin').exists():
        print("\n⚠️ User 'admin' already exists!")
        user = User.objects.get(username='admin')
        print(f"✅ Using existing user: {user.username}")
    else:
        user = User.objects.create_superuser(
            username='admin',
            email='bennymaish01@gmail.com',
            password='shiku2025',
            first_name='Shiku',
            last_name='Admin'
        )
        print("\n✅ Superuser created successfully!")
        print(f"   Username: admin")
        print(f"   Email: bennymaish01@gmail.com")
        print(f"   Password: shiku2025")
    
    print("\n" + "=" * 70)
    print("✅ RAILWAY SUPERUSER READY!")
    print("=" * 70)
    print("\n🚂 Your admin account on Railway:")
    print("   Username: admin")
    print("   Password: shiku2025")
    print("\n📝 Login at: http://127.0.0.1:3000/admin/")
    print("   (Once deployed, use your Railway URL)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nRun manually: python manage.py createsuperuser")

