# 📋 Complete Deployment Steps

## ⚠️ Important: Close and Reopen Terminal First!

Before running these commands, **close and reopen your terminal** so `gcloud` is recognized.

---

## ✅ Step 1: Set Up Cloud SQL Database

### Create Database Instance:

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

**⚠️ Replace `YOUR_USER_PASSWORD` with a password (can be same as root)**

### Get Connection Name:

```bash
gcloud sql instances describe shiku-db --format="value(connectionName)"
```

**💾 Save the connection name!** (Format: `PROJECT_ID:REGION:INSTANCE_NAME`)

---

## ✅ Step 2: Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**💾 Copy and save this secret key!**

---

## ✅ Step 3: Build Docker Image

```bash
docker build -t gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest .
```

**Note:** This takes 5-10 minutes the first time.

---

## ✅ Step 4: Push to Container Registry

```bash
gcloud auth configure-docker
docker push gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest
```

---

## ✅ Step 5: Deploy to Cloud Run

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
  --add-cloudsql-instances CONNECTION_NAME
```

**⚠️ Replace:**
- `YOUR_SECRET_KEY` with your secret key from Step 2
- `CONNECTION_NAME` with your connection name from Step 1

### Get Cloud Run URL:

```bash
gcloud run services describe shiku-beuty-hub --region us-central1 --format "value(status.url)"
```

**💾 Save this URL!**

---

## ✅ Step 6: Configure Database Connection

```bash
gcloud run services update shiku-beuty-hub \
  --region us-central1 \
  --update-env-vars "DATABASE_URL=postgresql://shiku_user:YOUR_PASSWORD@/shiku_db?host=/cloudsql/CONNECTION_NAME"
```

**⚠️ Replace:**
- `YOUR_PASSWORD` with your database user password
- `CONNECTION_NAME` with your connection name

---

## ✅ Step 7: Run Migrations

### Create Migration Job:

```bash
gcloud run jobs create migrate-shiku \
  --image gcr.io/shiku-beuty-hub/shiku-beauty-hub:latest \
  --region us-central1 \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False" \
  --set-env-vars "DATABASE_URL=postgresql://shiku_user:PASSWORD@/shiku_db?host=/cloudsql/CONNECTION_NAME" \
  --add-cloudsql-instances CONNECTION_NAME \
  --command python \
  --args manage.py,migrate
```

### Execute Migration:

```bash
gcloud run jobs execute migrate-shiku --region us-central1
```

---

## ✅ Step 8: Connect Firebase to Cloud Run

### Restore Cloud Run Configuration:

```bash
copy firebase.json.backup firebase.json
```

### Collect Static Files:

```bash
python manage.py collectstatic --noinput
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

---

## 🚀 Quick Deploy Script

Instead of running commands manually, you can use:

```bash
🚀 QUICK_DEPLOY_ALL.bat
```

This automates all steps above!

---

## 📝 Important Notes

1. **Close and reopen terminal** before running commands
2. **Save all passwords and keys** - you'll need them!
3. **Be patient** - database creation takes 5-10 minutes
4. **Docker build** takes 5-10 minutes the first time

---

**🚀 Ready? Close and reopen terminal, then run the commands above!**

