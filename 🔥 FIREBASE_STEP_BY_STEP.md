# 🔥 Firebase Deployment - Step by Step Guide

## 📋 Overview

We'll deploy your Django app using:
- **Google Cloud Run**: Hosts your Django backend (Docker container)
- **Firebase Hosting**: Serves static files and routes to Cloud Run

---

## ✅ STEP 1: Install Required Tools

### 1.1 Install Google Cloud SDK

**Windows:**
1. Download from: https://cloud.google.com/sdk/docs/install
2. Run the installer
3. Or use Chocolatey: `choco install gcloudsdk`

**Verify installation:**
```bash
gcloud --version
```

### 1.2 Install Firebase CLI

```bash
npm install -g firebase-tools
```

**Verify installation:**
```bash
firebase --version
```

### 1.3 Install Docker (if not installed)

**Windows:**
- Download Docker Desktop: https://www.docker.com/products/docker-desktop
- Install and restart your computer

**Verify installation:**
```bash
docker --version
```

---

## ✅ STEP 2: Login to Google Cloud & Firebase

### 2.1 Login to Google Cloud

```bash
gcloud auth login
```

This will open your browser - login with your Google account.

### 2.2 Set up Google Cloud Project

```bash
# Create a new project (or use existing)
gcloud projects create shiku-beauty-hub --name="Shiku Beauty Hub"

# Set as current project
gcloud config set project shiku-beauty-hub

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
# Link your project to a billing account (Free tier available!)
```

### 2.3 Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

### 2.4 Login to Firebase

```bash
firebase login
```

This will open your browser - login with the same Google account.

### 2.5 Initialize Firebase Project

```bash
# Navigate to your project folder
cd "C:\shiku salon"

# Initialize Firebase
firebase init hosting
```

**When prompted:**
- ✅ Select: **Use an existing project**
- ✅ Select: **shiku-beauty-hub** (or create new)
- ✅ Public directory: **staticfiles**
- ✅ Single-page app: **No**
- ✅ Overwrite index.html: **No**

---

## ✅ STEP 3: Set Up Database (Cloud SQL PostgreSQL)

### 3.1 Create Cloud SQL Instance

```bash
gcloud sql instances create shiku-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_STRONG_PASSWORD_HERE
```

**⚠️ Replace `YOUR_STRONG_PASSWORD_HERE` with a strong password!**
**💾 Save this password - you'll need it!**

**Note:** This may take 5-10 minutes. Be patient!

### 3.2 Create Database

```bash
gcloud sql databases create shiku_db --instance=shiku-db
```

### 3.3 Create Database User

```bash
gcloud sql users create shiku_user \
  --instance=shiku-db \
  --password=YOUR_USER_PASSWORD
```

**⚠️ Replace `YOUR_USER_PASSWORD` with a password (can be same as root password)**

### 3.4 Get Connection Name

```bash
gcloud sql instances describe shiku-db --format="value(connectionName)"
```

**💾 Save the connection name!** (Format: `PROJECT_ID:REGION:INSTANCE_NAME`)

---

## ✅ STEP 4: Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**💾 Copy and save this secret key!** You'll need it in the next step.

---

## ✅ STEP 5: Build and Deploy to Cloud Run

### 5.1 Build Docker Image

```bash
# Make sure you're in the project directory
cd "C:\shiku salon"

# Build the Docker image
docker build -t gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest .
```

**Note:** This may take 5-10 minutes the first time.

### 5.2 Push to Google Container Registry

```bash
# Configure Docker to use gcloud
gcloud auth configure-docker

# Push the image
docker push gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest
```

### 5.3 Deploy to Cloud Run

```bash
gcloud run deploy shiku-beuty-hub \
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
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY_HERE,DEBUG=False" \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db
```

**⚠️ Replace:**
- `YOUR_SECRET_KEY_HERE` with the secret key from Step 4
- `PROJECT_ID:us-central1:shiku-db` with your connection name from Step 3.4

**Example:**
```bash
gcloud run deploy shiku-beuty-hub \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "SECRET_KEY=django-insecure-abc123...,DEBUG=False" \
  --add-cloudsql-instances shiku-beauty-hub:us-central1:shiku-db
```

### 5.4 Get Cloud Run URL

After deployment, you'll see a URL like:
```
https://shiku-beuty-hub-xxxxx-uc.a.run.app
```

**💾 Save this URL!**

---

## ✅ STEP 6: Configure Database Connection

### 6.1 Update Settings for Cloud SQL

We need to update your Django settings to use Cloud SQL. The connection string format is:

```
postgresql://USERNAME:PASSWORD@/DATABASE_NAME?host=/cloudsql/CONNECTION_NAME
```

### 6.2 Set Database URL Environment Variable

```bash
gcloud run services update shiku-beuty-hub \
  --region us-central1 \
  --update-env-vars "DATABASE_URL=postgresql://shiku_user:YOUR_PASSWORD@/shiku_db?host=/cloudsql/PROJECT_ID:us-central1:shiku-db"
```

**⚠️ Replace:**
- `YOUR_PASSWORD` with your database user password
- `PROJECT_ID:us-central1:shiku-db` with your connection name

---

## ✅ STEP 7: Run Migrations

### 7.1 Create Migration Job

```bash
gcloud run jobs create migrate-shiku \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False" \
  --set-env-vars "DATABASE_URL=postgresql://shiku_user:PASSWORD@/shiku_db?host=/cloudsql/PROJECT_ID:us-central1:shiku-db" \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db \
  --command python \
  --args manage.py,migrate
```

### 7.2 Execute Migration

```bash
gcloud run jobs execute migrate-shiku --region us-central1
```

---

## ✅ STEP 8: Update Firebase Configuration

### 8.1 Update firebase.json

Make sure your `firebase.json` has the correct service ID:

```json
{
  "hosting": {
    "public": "staticfiles",
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "shiku-beuty-hub",
          "region": "us-central1"
        }
      }
    ]
  }
}
```

### 8.2 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## ✅ STEP 9: Deploy Firebase Hosting

```bash
firebase deploy --only hosting
```

**🎉 Your website is now live!**

You'll get a URL like: `https://shiku-beauty-hub.web.app`

---

## ✅ STEP 10: Create Admin User

### 10.1 Create Superuser Job

```bash
gcloud run jobs create createsuperuser-shiku \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False" \
  --set-env-vars "DATABASE_URL=YOUR_DATABASE_URL" \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db \
  --command python \
  --args manage.py,createsuperuser \
  --interactive
```

### 10.2 Execute Superuser Creation

```bash
gcloud run jobs execute createsuperuser-shiku --region us-central1
```

Follow the prompts to create your admin account.

---

## 🌐 Access Your Website

### Main Website:
```
https://shiku-beauty-hub.web.app
```

### Admin Panel:
```
https://shiku-beauty-hub.web.app/admin/
```

---

## 🔄 Updating Your Website

When you make changes:

1. **Build new Docker image:**
```bash
docker build -t gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest .
```

2. **Push to registry:**
```bash
docker push gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest
```

3. **Deploy to Cloud Run:**
```bash
gcloud run deploy shiku-beuty-hub \
  --image gcr.io/shiku-beauty-hub/shiku-beauty-hub:latest \
  --region us-central1
```

4. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

5. **Deploy Firebase Hosting:**
```bash
firebase deploy --only hosting
```

---

## 🆘 Troubleshooting

### "Service not found" error:
- Check Cloud Run service name matches `firebase.json`
- Verify service is deployed in same region (us-central1)

### Database connection errors:
- Check Cloud SQL instance is running
- Verify connection name format
- Check environment variables are set correctly

### Static files not loading:
- Run `collectstatic` before deploying
- Check `STATIC_ROOT` in settings.py

### 502 Bad Gateway:
- Check Cloud Run logs: `gcloud logging read "resource.type=cloud_run_revision" --limit 50`
- Verify container starts successfully
- Check health endpoint: `/health/`

---

## 💰 Pricing (Free Tier)

- **Cloud Run**: 2 million requests/month FREE
- **Cloud SQL**: db-f1-micro instance FREE (first 2 instances)
- **Firebase Hosting**: 10 GB storage, 360 MB/day bandwidth FREE

**Your site will be FREE for most traffic!** 🎉

---

## ✅ Checklist

- [ ] Google Cloud SDK installed
- [ ] Firebase CLI installed
- [ ] Docker installed
- [ ] Logged into Google Cloud
- [ ] Logged into Firebase
- [ ] Project created
- [ ] APIs enabled
- [ ] Cloud SQL instance created
- [ ] Database and user created
- [ ] Secret key generated
- [ ] Docker image built
- [ ] Deployed to Cloud Run
- [ ] Database configured
- [ ] Migrations run
- [ ] Static files collected
- [ ] Firebase Hosting deployed
- [ ] Admin user created
- [ ] Website accessible

---

**🚀 You're all set! Your Django website is now hosted on Firebase!** 💎✨

