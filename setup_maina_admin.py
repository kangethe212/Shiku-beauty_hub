#!/usr/bin/env python
"""
Setup Maina as superadmin with password Benny@123
This script can be run on Railway deployment to ensure Maina admin exists
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.contrib.auth.models import User

# Create or update Maina as superadmin
username = 'Maina'
email = 'bennymaish01@gmail.com'
password = 'Benny@123'

maina, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': email,
        'is_superuser': True,
        'is_staff': True,
        'is_active': True,
    }
)

# Always update to ensure correct settings
maina.email = email
maina.is_superuser = True
maina.is_staff = True
maina.is_active = True
maina.set_password(password)
maina.save()

if created:
    print(f"✅ Created superadmin: {username}")
else:
    print(f"✅ Updated superadmin: {username}")

print(f"   Email: {email}")
print(f"   Password: {password}")
print(f"   Superuser: {maina.is_superuser}")
print(f"   Staff: {maina.is_staff}")
print(f"   Active: {maina.is_active}")

