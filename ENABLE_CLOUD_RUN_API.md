# 🔧 Enable Cloud Run API - Step by Step

## 🎯 Goal
Enable Cloud Run API so Firebase Hosting can route to Cloud Run services.

---

## ✅ Method 1: Web Console (Easiest - No Installation Needed)

### Step 1: Open the API Enable Page

**Click this link:**
```
https://console.developers.google.com/apis/api/run.googleapis.com/overview?project=140804076783
```

Or manually:
1. Go to: https://console.cloud.google.com/
2. Select project: **shiku-beuty-hub**
3. Navigate to: **APIs & Services** → **Library**
4. Search for: **Cloud Run Admin API**
5. Click on it
6. Click **Enable**

### Step 2: Wait for Activation

- Wait **2-3 minutes** for the API to activate
- You'll see a green checkmark when it's enabled

### Step 3: Verify It's Enabled

You should see:
- ✅ **Status: Enabled**
- ✅ Green checkmark icon

### Step 4: Deploy to Firebase

Once enabled, run:
```bash
firebase deploy --only hosting
```

---

## ✅ Method 2: Using Google Cloud SDK (If Installed)

If you install Google Cloud SDK later, you can enable it via command line:

```bash
# Login
gcloud auth login

# Set project
gcloud config set project shiku-beuty-hub

# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Verify
gcloud services list --enabled | grep run
```

---

## 🔍 How to Check if API is Enabled

### Via Web Console:
1. Go to: https://console.cloud.google.com/apis/library?project=140804076783
2. Search for "Cloud Run Admin API"
3. Check if it shows "Enabled"

### Via Firebase:
Try deploying - if API is enabled, deployment will proceed.

---

## ⚠️ Important Notes

1. **Billing Required:** Cloud Run API requires billing to be enabled on your Google Cloud project
2. **Free Tier:** Google Cloud has a generous free tier - you likely won't be charged for low traffic
3. **Activation Time:** API activation can take 2-5 minutes

---

## 🚀 After Enabling

Once the API is enabled:

1. **Deploy Firebase Hosting:**
   ```bash
   firebase deploy --only hosting
   ```

2. **Next Steps:**
   - Deploy Django backend to Cloud Run (see: `🔥 FIREBASE_STEP_BY_STEP.md`)
   - Run migrations
   - Create admin user

---

## 🆘 Troubleshooting

### "Billing account required"
**Solution:** 
1. Go to: https://console.cloud.google.com/billing
2. Link a billing account to your project
3. Free tier is available - you won't be charged for low usage

### "Permission denied"
**Solution:** Make sure you're logged in with the account that owns the project

### "API not found"
**Solution:** Make sure you're in the correct project (shiku-beuty-hub)

---

**📝 Ready? Click the link above and enable the API!** 🚀

