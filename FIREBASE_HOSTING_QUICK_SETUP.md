# 🔥 Firebase Hosting - Quick Setup Guide

## ✅ Current Status

- ✅ Firebase CLI installed (v14.24.1)
- ✅ Logged in as: bennymaish01@gmail.com
- ✅ Project exists: shiku-beuty-hub
- ✅ firebase.json configured
- ✅ Static files collected

---

## 🚀 Quick Deployment (3 Steps)

### Step 1: Initialize Firebase Project (One-time)

If `.firebaserc` doesn't exist, run:

```bash
firebase init hosting
```

**When prompted:**
- ✅ Select: **Use an existing project**
- ✅ Choose: **shiku-beuty-hub**
- ✅ Public directory: **staticfiles**
- ✅ Single-page app: **No** (Django has multiple pages)
- ✅ Overwrite index.html: **No**

**OR use the automated script:**
```bash
deploy_firebase_hosting.bat
```

---

### Step 2: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This creates the `staticfiles/` directory that Firebase Hosting will serve.

---

### Step 3: Deploy to Firebase Hosting

```bash
firebase deploy --only hosting
```

**That's it!** Your static files are now live! 🎉

---

## 🌐 Your Live URLs

After deployment, your site will be available at:

- **Primary:** https://shiku-beuty-hub.web.app
- **Alternative:** https://shiku-beuty-hub.firebaseapp.com

---

## ⚠️ Important Notes

### Static Files Only

Firebase Hosting alone can only serve **static files** (HTML, CSS, JS, images). 

For your **Django app** to work fully, you need:

1. **Google Cloud Run** - Hosts your Django backend
2. **Firebase Hosting** - Serves static files and routes to Cloud Run

Your `firebase.json` is already configured for Cloud Run integration!

---

## 🔄 Updating Your Site

When you make changes:

1. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Deploy:**
   ```bash
   firebase deploy --only hosting
   ```

---

## 🆘 Troubleshooting

### "Project not initialized"
**Solution:** Run `firebase init hosting` or use `deploy_firebase_hosting.bat`

### "No static files found"
**Solution:** Run `python manage.py collectstatic --noinput` first

### "Permission denied"
**Solution:** Make sure you're logged in: `firebase login`

### "Project not found"
**Solution:** Verify project exists: `firebase projects:list`

---

## 📋 Manual Setup (If Script Doesn't Work)

### 1. Set Firebase Project
```bash
firebase use shiku-beuty-hub
```

### 2. Initialize Hosting
```bash
firebase init hosting
```

**Select:**
- Use existing project: `shiku-beuty-hub`
- Public directory: `staticfiles`
- Single-page app: `No`
- Overwrite index.html: `No`

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Deploy
```bash
firebase deploy --only hosting
```

---

## ✅ Checklist

- [ ] Firebase CLI installed ✅
- [ ] Logged in to Firebase ✅
- [ ] Project selected (shiku-beuty-hub) ✅
- [ ] Firebase initialized (`.firebaserc` exists)
- [ ] Static files collected
- [ ] Deployed to Firebase Hosting
- [ ] Website accessible

---

## 🎯 Next Steps

After deploying static files:

1. **Deploy Django backend to Cloud Run** (see: `🔥 FIREBASE_STEP_BY_STEP.md`)
2. **Connect Firebase Hosting to Cloud Run** (already configured in `firebase.json`)
3. **Run migrations** on Cloud Run
4. **Create admin user**

---

**🚀 Ready to deploy? Run: `deploy_firebase_hosting.bat`**

Or follow the manual steps above!

