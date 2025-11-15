# 🚀 Complete Firebase + Cloud Run Deployment Guide

## 📋 Overview

This guide will help you deploy your full Django application to Firebase + Google Cloud Run.

---

## ✅ Step 1: Enable Cloud Run API

### Option A: Web Console (Easiest)

1. **Open this link:**
   ```
   https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=140804076783
   ```

2. **Click "ENABLE"**

3. **Wait 2-3 minutes** for activation

### Option B: Command Line (If gcloud is installed)

```bash
gcloud services enable run.googleapis.com --project=shiku-beuty-hub
```

---

## ✅ Step 2: Install Google Cloud SDK (If Not Installed)

### Windows:

1. **Download:** https://cloud.google.com/sdk/docs/install
2. **Run installer**
3. **Restart terminal**

### Verify Installation:

```bash
gcloud --version
```

### Login:

```bash
gcloud auth login
gcloud config set project shiku-beuty-hub
```

---

## ✅ Step 3: Set Up Database (Cloud SQL PostgreSQL)

### Create Cloud SQL Instance:

```bash
gcloud sql instances create shiku-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_STRONG_PASSWORD
```

**⚠️ Replace `YOUR_STRONG_PASSWORD` with a strong password!**
**💾 Save this password!**

**Note:** This takes 5-10 minutes. Be patient!

### Create Database:

```bash
gcloud sql databases create shiku_db --instance=shiku-db
```

### Create Database User:

```bash
gcloud sql users create shiku_user \
  --instance=shiku-db \
  --password=YOUR_USER_PASSWORD
```

### Get Connection Name:

```bash
gcloud sql instances describe shiku-db --format="value(connectionName)"
```

**💾 Save the connection name!** (Format: `PROJECT_ID:REGION:INSTANCE_NAME`)

---

## ✅ Step 4: Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**💾 Copy and save this secret key!**

---

## ✅ Step 5: Build and Push Docker Image

### Build Docker Image:

```bash
docker build -t gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest .
```

**Note:** This takes 5-10 minutes the first time.

### Configure Docker for Google Cloud:

```bash
gcloud auth configure-docker
```

### Push to Google Container Registry:

```bash
docker push gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest
```

---

## ✅ Step 6: Deploy to Cloud Run

### Get Connection Name:

```bash
gcloud sql instances describe shiku-db --format="value(connectionName)"
```

### Deploy:

```bash
gcloud run deploy shiku-beuty-hub \
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False" \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db
```

**⚠️ Replace:**
- `YOUR_SECRET_KEY` with your secret key from Step 4
- `PROJECT_ID:us-central1:shiku-db` with your connection name

### Get Cloud Run URL:

After deployment, you'll see a URL like:
```
https://shiku-beuty-hub-xxxxx-uc.a.run.app
```

**💾 Save this URL!**

---

## ✅ Step 7: Configure Database Connection

### Set Database URL:

```bash
gcloud run services update shiku-beuty-hub \
  --region us-central1 \
  --update-env-vars "DATABASE_URL=postgresql://shiku_user:YOUR_PASSWORD@/shiku_db?host=/cloudsql/PROJECT_ID:us-central1:shiku-db"
```

**⚠️ Replace:**
- `YOUR_PASSWORD` with your database user password
- `PROJECT_ID:us-central1:shiku-db` with your connection name

---

## ✅ Step 8: Run Migrations

### Create Migration Job:

```bash
gcloud run jobs create migrate-shiku \
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False" \
  --set-env-vars "DATABASE_URL=postgresql://shiku_user:PASSWORD@/shiku_db?host=/cloudsql/PROJECT_ID:us-central1:shiku-db" \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db \
  --command python \
  --args manage.py,migrate
```

### Execute Migration:

```bash
gcloud run jobs execute migrate-shiku --region us-central1
```

---

## ✅ Step 9: Create Admin User

### Create Superuser Job:

```bash
gcloud run jobs create createsuperuser-shiku \
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False" \
  --set-env-vars "DATABASE_URL=YOUR_DATABASE_URL" \
  --add-cloudsql-instances PROJECT_ID:us-central1:shiku-db \
  --command python \
  --args manage.py,createsuperuser \
  --interactive
```

### Execute:

```bash
gcloud run jobs execute createsuperuser-shiku --region us-central1
```

Follow the prompts to create your admin account.

---

## ✅ Step 10: Connect Firebase Hosting to Cloud Run

### Restore Cloud Run Configuration:

```bash
copy firebase.json.backup firebase.json
```

### Update firebase.json:

Make sure the `serviceId` matches your Cloud Run service name:

```json
{
  "hosting": {
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

### Deploy Firebase Hosting:

```bash
firebase deploy --only hosting
```

---

## 🌐 Access Your Website

### Main Website:
```
https://shiku-beuty-hub.web.app
```

### Admin Panel:
```
https://shiku-beuty-hub.web.app/admin/
```

### Direct Cloud Run URL:
```
https://shiku-beuty-hub-xxxxx-uc.a.run.app
```

---

## 🔄 Updating Your Site

When you make changes:

1. **Build new image:**
   ```bash
   docker build -t gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest .
   ```

2. **Push:**
   ```bash
   docker push gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest
   ```

3. **Deploy:**
   ```bash
   gcloud run deploy shiku-beuty-hub \
     --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest \
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

### "Service not found"
- Check Cloud Run service name matches `firebase.json`
- Verify service is deployed in same region

### "Database connection failed"
- Check Cloud SQL instance is running
- Verify connection name format
- Check environment variables

### "Permission denied"
- Make sure you're logged in: `gcloud auth login`
- Check project permissions

---

## ✅ Checklist

- [ ] Cloud Run API enabled
- [ ] Google Cloud SDK installed
- [ ] Logged into Google Cloud
- [ ] Cloud SQL instance created
- [ ] Database and user created
- [ ] Secret key generated
- [ ] Docker image built and pushed
- [ ] Cloud Run service deployed
- [ ] Database configured
- [ ] Migrations run
- [ ] Admin user created
- [ ] Firebase Hosting connected to Cloud Run
- [ ] Website accessible
- [ ] Admin panel working

---

**🚀 Follow these steps in order to complete your deployment!**

