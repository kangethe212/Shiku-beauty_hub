# 🔥 Firebase Hosting Deployment - Fix Required

## ❌ Current Error

```
Error: Cloud Run Admin API has not been used in project 140804076783 before or it is disabled.
```

## 🎯 Two Options to Fix

---

## Option 1: Enable Cloud Run API (Recommended for Full Deployment)

Your `firebase.json` is configured to route to Cloud Run, but the API needs to be enabled first.

### Enable via Google Cloud Console:

1. **Open this link:**
   ```
   https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=140804076783
   ```

2. **Click "Enable"**

3. **Wait 2-3 minutes** for the API to activate

4. **Deploy again:**
   ```bash
   firebase deploy --only hosting
   ```

### OR Enable via Command Line:

```bash
# Login to Google Cloud
gcloud auth login

# Set project
gcloud config set project shiku-beuty-hub

# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Wait 2-3 minutes, then deploy
firebase deploy --only hosting
```

---

## Option 2: Deploy Static Files Only (Quick Fix)

If you just want to deploy static files now (without Cloud Run routing):

### Step 1: Backup current firebase.json
```bash
copy firebase.json firebase.json.with-cloudrun
```

### Step 2: Use static-only configuration
```bash
copy firebase.json.static-only firebase.json
```

### Step 3: Deploy
```bash
firebase deploy --only hosting
```

### Step 4: Restore Cloud Run config later
When you're ready for full deployment:
```bash
copy firebase.json.with-cloudrun firebase.json
```

---

## 📋 What Each Option Does

### Option 1 (Enable Cloud Run API):
- ✅ Enables full Firebase Hosting + Cloud Run integration
- ✅ Your Django app can be deployed to Cloud Run later
- ✅ Firebase will route requests to Cloud Run automatically
- ⚠️ Requires Google Cloud account with billing enabled

### Option 2 (Static Files Only):
- ✅ Quick deployment of static files
- ✅ No Cloud Run API needed
- ✅ Works immediately
- ⚠️ Only serves static files (no Django backend)
- ⚠️ Need to update firebase.json later for full app

---

## 🚀 Recommended: Enable Cloud Run API

Since you're planning to deploy the full Django app, **Option 1 is recommended**.

### Quick Steps:

1. **Enable API:**
   - Visit: https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=140804076783
   - Click "Enable"
   - Wait 2-3 minutes

2. **Deploy:**
   ```bash
   firebase deploy --only hosting
   ```

3. **Next:** Deploy Django backend to Cloud Run (see: `🔥 FIREBASE_STEP_BY_STEP.md`)

---

## ✅ After Fixing

Once deployed, your static files will be live at:
- https://shiku-beuty-hub.web.app
- https://shiku-beuty-hub.firebaseapp.com

---

**Choose an option above and continue!** 🚀

