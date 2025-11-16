#!/usr/bin/env python
"""
Script to upload media files to Railway
Note: Railway uses ephemeral storage, so media files will be lost on redeploy
For production, consider using cloud storage (AWS S3, Cloudinary, etc.)
"""
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / 'media'

print("=" * 70)
print("  UPLOADING MEDIA FILES TO RAILWAY")
print("=" * 70)

if not MEDIA_DIR.exists():
    print(f"❌ Media directory not found: {MEDIA_DIR}")
    sys.exit(1)

print(f"\n✓ Media directory found: {MEDIA_DIR}")

# Count files
total_files = 0
for root, dirs, files in os.walk(MEDIA_DIR):
    total_files += len([f for f in files if not f.startswith('.')])

print(f"✓ Found {total_files} media files")

print("\n" + "=" * 70)
print("  IMPORTANT: Railway Ephemeral Storage")
print("=" * 70)
print("\n⚠️  WARNING: Railway uses ephemeral storage!")
print("   Media files uploaded to Railway will be LOST when:")
print("   - The service is redeployed")
print("   - The service restarts")
print("   - The service is updated")
print("\n💡 RECOMMENDED: Use cloud storage for production:")
print("   - AWS S3")
print("   - Cloudinary")
print("   - Google Cloud Storage")
print("   - Azure Blob Storage")
print("\n📝 For now, you can:")
print("   1. Upload media files through Django admin on Railway")
print("   2. Use Railway volumes (paid feature)")
print("   3. Set up cloud storage (recommended)")

print("\n" + "=" * 70)
print("  OPTION 1: Upload via Django Admin")
print("=" * 70)
print("\n1. Go to your Railway admin panel")
print("2. Navigate to the models (Hairstyles, Perfumes, Clothing, etc.)")
print("3. Edit each item and upload images")
print("\nThis will store files in Railway's ephemeral storage.")

print("\n" + "=" * 70)
print("  OPTION 2: Use Railway CLI to Copy Files")
print("=" * 70)
print("\nIf you have Railway CLI installed:")
print(f"  railway run mkdir -p /app/media")
print(f"  railway run cp -r {MEDIA_DIR}/* /app/media/")
print("\n⚠️  Files will still be lost on redeploy!")

print("\n" + "=" * 70)
print("  RECOMMENDED: Cloud Storage Setup")
print("=" * 70)
print("\nFor production, set up cloud storage:")
print("1. Create account on Cloudinary (free tier available)")
print("2. Install: pip install django-cloudinary-storage")
print("3. Configure in settings.py")
print("4. Update MEDIA_ROOT and MEDIA_URL")
print("\nThis ensures media files persist and scale properly.")

print("\n" + "=" * 70)
print("  CURRENT STATUS")
print("=" * 70)
print(f"\n✓ Media files configured to be served")
print(f"✓ {total_files} files ready locally")
print(f"⚠️  Media files need to be uploaded to Railway")
print(f"💡 Use Django admin or set up cloud storage")

