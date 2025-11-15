# 🚀 Firebase + Google Cloud Run Deployment Guide

## 📋 Overview

Your Django application will be deployed using:
- **Google Cloud Run**: Hosts the Django backend (Docker container)
- **Firebase Hosting**: Serves static files and routes requests to Cloud Run

---

## ✅ Prerequisites

1. **Google Cloud Account** (with billing enabled)
   - Go to: https://cloud.google.com/
   - Create account or login
   - Enable billing (Firebase/Cloud Run has a free tier)

2. **Firebase Account**
   - Go to: https://console.firebase.google.com/
   - Create project (or use existing)
   - Link with Google Cloud project

3. **Install Required Tools:**

```bash
# Install Google Cloud SDK
# Windows: Download from https://cloud.google.com/sdk/docs/install
# Or use: choco install gcloudsdk (if you have Chocolatey)

# Install Firebase CLI
npm install -g firebase-tools

# Verify installations
gcloud --version
firebase --version
```

---

## 🔧 Step 1: Set Up Google Cloud Project

### 1.1 Login to Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create shiku-beauty-hub --name="Shiku Beauty Hub"

# Set as current project
gcloud config set project shiku-beauty-hub

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 1.2 Link Firebase to Google Cloud

1. Go to: https://console.firebase.google.com/
2. Click "Add project" or select existing
3. Choose "Use an existing Google Cloud project"
4. Select: `shiku-beauty-hub`
5. Click "Continue"

---

## 🔧 Step 2: Configure Firebase

### 2.1 Initialize Firebase in Your Project

```bash
# Navigate to your project directory
cd "C:\shiku salon"

# Login to Firebase
firebase login

# Initialize Firebase (choose Hosting)
firebase init

# When prompted:
# ✅ Select: Hosting
# ✅ Select: Use existing project (shiku-beauty-hub)
# ✅ Public directory: staticfiles (or build if you use one)
# ✅ Single-page app: No (Django has multiple pages)
# ✅ Overwrite index.html: No
```

### 2.2 Update firebase.json (Already Created!)

Your `firebase.json` is already configured! Just update the `serviceId` if needed:

```json
{
  "hosting": {
    "public": "staticfiles",
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "shiku-beauty-hub",  // Update this after deploying Cloud Run
          "region": "us-central1"
        }
      }
    ]
  }
}
```

---

## 🔧 Step 3: Set Up Database (PostgreSQL)

### 3.1 Create Cloud SQL PostgreSQL Instance

```bash
# Create Cloud SQL instance (First 2 instances are free!)
gcloud sql instances create shiku-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_STRONG_PASSWORD
```

### 3.2 Create Database

```bash
# Create database
gcloud sql databases create shiku_db --instance=shiku-db

# Create user
gcloud sql users create shiku_user \
  --instance=shiku-db \
  --password=YOUR_USER_PASSWORD
```

### 3.3 Get Connection String

```bash
# Get connection name
gcloud sql instances describe shiku-db --format="value(connectionName)"

# Save the connection name (format: PROJECT_ID:REGION:INSTANCE_NAME)
# Example: shiku-beauty-hub:us-central1:shiku-db
```

---

## 🔧 Step 4: Deploy to Google Cloud Run

### 4.1 Set Environment Variables

```bash
# Set secret key (generate a new one!)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Save this secret key - you'll need it!
```

### 4.2 Build and Push Docker Image

```bash
# Build Docker image
docker build -t gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest .

# Push to Google Container Registry
docker push gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest
```

**OR use Cloud Build (Automated):**

```bash
# Submit build to Cloud Build
gcloud builds submit --config cloudbuild.yaml .
```

### 4.3 Deploy to Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy shiku-beauty-hub \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False \
  --set-env-vars DATABASE_URL=postgresql://shiku_user:PASSWORD@/shiku_db?host=/cloudsql/PROJECT_ID:us-central1:shiku-db \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db
```

### 4.4 Get Cloud Run URL

```bash
# Get service URL
gcloud run services describe shiku-beauty-hub \
  --region us-central1 \
  --format "value(status.url)"
```

**Save this URL!** Example: `https://shiku-beauty-hub-xxxxx-uc.a.run.app`

---

## 🔧 Step 5: Update firebase.json with Cloud Run URL

Edit `firebase.json`:

```json
{
  "hosting": {
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "shiku-beauty-hub",
          "region": "us-central1"
        }
      }
    ]
  }
}
```

---

## 🔧 Step 6: Collect Static Files and Deploy Firebase Hosting

### 6.1 Collect Static Files

```bash
# Collect static files locally
python manage.py collectstatic --noinput

# This creates the staticfiles/ directory (used by Firebase Hosting)
```

### 6.2 Deploy Firebase Hosting

```bash
# Deploy to Firebase Hosting
firebase deploy --only hosting
```

---

## 🔧 Step 7: Run Migrations on Cloud Run

```bash
# Run migrations on Cloud Run service
gcloud run jobs create migrate-shiku \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False \
  --set-env-vars DATABASE_URL=YOUR_DATABASE_URL \
  --command python \
  --args manage.py,migrate

# Execute migration job
gcloud run jobs execute migrate-shiku --region us-central1

# OR use Cloud Run exec
gcloud run services update shiku-beauty-hub \
  --region us-central1 \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db
```

**Alternative: SSH into container and run migrations**

```bash
# Create admin user (interactive)
gcloud run jobs create createsuperuser-shiku \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False \
  --set-env-vars DATABASE_URL=YOUR_DATABASE_URL \
  --command python \
  --args manage.py,createsuperuser \
  --interactive

gcloud run jobs execute createsuperuser-shiku --region us-central1
```

---

## 🔧 Step 8: Transfer Data to Cloud SQL

### 8.1 Export from Railway/Local PostgreSQL

```bash
# Export data from Railway PostgreSQL
pg_dump -h yamanote.proxy.rlwy.net -p 27057 -U postgres -d railway > backup.sql

# Or export specific tables using Django
python manage.py dumpdata > backup.json
```

### 8.2 Import to Cloud SQL

```bash
# Import to Cloud SQL
gcloud sql import sql shiku-db gs://YOUR_BUCKET/backup.sql \
  --database=shiku_db \
  --user=shiku_user

# OR use Django loaddata
python manage.py loaddata backup.json
```

---

## 🌐 Step 9: Access Your Website

### Your Firebase URL:
```
https://shiku-beauty-hub.web.app
```

### Your Cloud Run URL (Direct):
```
https://shiku-beauty-hub-xxxxx-uc.a.run.app
```

### Admin Panel:
```
https://shiku-beauty-hub.web.app/admin/
```

---

## 🔑 Environment Variables Setup

### Set in Cloud Run:

```bash
gcloud run services update shiku-beauty-hub \
  --region us-central1 \
  --update-env-vars SECRET_KEY=YOUR_SECRET_KEY \
  --update-env-vars DEBUG=False \
  --update-env-vars DATABASE_URL=YOUR_DATABASE_URL \
  --update-env-vars TELEGRAM_BOT_TOKEN=YOUR_TOKEN \
  --update-env-vars TELEGRAM_CHAT_ID=YOUR_CHAT_ID
```

**Or use Google Secret Manager (Recommended):**

```bash
# Create secrets
echo -n "YOUR_SECRET_KEY" | gcloud secrets create django-secret-key --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding django-secret-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## 📊 Monitoring & Logs

### View Logs:

```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Firebase Hosting logs
firebase hosting:channel:list
```

### Monitor in Console:

- **Cloud Run**: https://console.cloud.google.com/run
- **Firebase**: https://console.firebase.google.com/
- **Cloud SQL**: https://console.cloud.google.com/sql

---

## 🎯 Quick Deployment Script

Create `deploy.bat` (Windows):

```batch
@echo off
echo 🚀 Deploying Shiku Beauty Hub to Firebase + Cloud Run...

echo.
echo 📦 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo 🐳 Building Docker image...
docker build -t gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest .

echo.
echo 📤 Pushing to Container Registry...
docker push gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest

echo.
echo 🚢 Deploying to Cloud Run...
gcloud run deploy shiku-beauty-hub ^
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --port 8080

echo.
echo 🔥 Deploying Firebase Hosting...
firebase deploy --only hosting

echo.
echo ✅ Deployment complete!
echo 🌐 Your website: https://shiku-beauty-hub.web.app
pause
```

---

## 💰 Pricing (Free Tier)

### Google Cloud Run (FREE):
- **2 million requests/month** free
- **400,000 GB-seconds** compute time free
- **200,000 CPU-seconds** free

### Cloud SQL (FREE):
- **db-f1-micro** instance: FREE for first 2 instances
- Storage: Pay as you go (very cheap)

### Firebase Hosting (FREE):
- **10 GB storage** free
- **360 MB/day** bandwidth free

**Your site will be FREE for most traffic!** 🎉

---

## 🆘 Troubleshooting

### "Service not found" error:
- Check Cloud Run service name matches `firebase.json`
- Verify service is deployed in same region

### Database connection errors:
- Check Cloud SQL instance is running
- Verify connection name format
- Check firewall rules (Cloud SQL should allow Cloud Run)

### Static files not loading:
- Run `collectstatic` before deploying
- Check `STATIC_ROOT` in settings.py
- Verify Firebase Hosting `public` directory

### 502 Bad Gateway:
- Check Cloud Run logs: `gcloud logging read`
- Verify container starts successfully
- Check health endpoint: `/health/`

---

## ✅ Success Checklist

- [ ] Google Cloud project created
- [ ] Firebase project linked
- [ ] Cloud SQL PostgreSQL created
- [ ] Docker image built and pushed
- [ ] Cloud Run service deployed
- [ ] Firebase Hosting configured
- [ ] Static files collected
- [ ] Migrations run
- [ ] Data transferred
- [ ] Environment variables set
- [ ] Website accessible
- [ ] Admin panel working

---

## 🎉 You're All Set!

Your Django website is now hosted on Firebase + Google Cloud Run!

**Your Live URL:** `https://shiku-beauty-hub.web.app`

**Admin:** `https://shiku-beauty-hub.web.app/admin/`

---

## 📞 Need Help?

- **Google Cloud Docs**: https://cloud.google.com/docs
- **Firebase Docs**: https://firebase.google.com/docs
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Django on Cloud Run**: https://cloud.google.com/python/django/run

---

**🚀 Good luck with your deployment!** 💎✨

