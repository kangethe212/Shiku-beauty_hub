# 🚀 Deploy Frontend to Firebase Hosting

## 📋 Overview

This guide will help you deploy your static frontend files to Firebase Hosting while keeping your Django backend on Railway.

## ✅ Prerequisites

1. Firebase CLI installed: `npm install -g firebase-tools`
2. Firebase project configured: `shiku-beuty-hub`
3. Static files collected: `python manage.py collectstatic`

## 🔧 Setup Steps

### Step 1: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This collects all CSS, JS, and static assets into the `staticfiles/` directory.

### Step 2: Deploy to Firebase Hosting

```bash
# Login to Firebase (if not already)
firebase login

# Deploy static files
firebase deploy --only hosting
```

### Step 3: Access Your Site

Your site will be available at:
- **Firebase URL**: https://shiku-beuty-hub.web.app
- **Firebase URL (Alt)**: https://shiku-beuty-hub.firebaseapp.com

## ⚠️ Important Notes

### Current Configuration

The `firebase.json` is configured to:
- Serve static files from `staticfiles/` directory
- All routes redirect to `/index.html` (for static site)

### For Django Backend Integration

Since Django renders templates server-side, you have two options:

#### Option 1: Static Site Only (Current Setup)
- Only static files (CSS, JS, images) are served
- HTML templates won't work (they need Django)
- Good for: Static assets, CDN for media files

#### Option 2: Hybrid Setup (Recommended)
- Deploy Django backend to Railway
- Use Firebase Hosting for static assets only
- Configure Railway to serve Django templates
- Update `firebase.json` to proxy API requests to Railway

### Recommended: Full Railway Deployment

For a Django app, it's better to deploy everything to Railway:
- Django backend serves templates
- Static files served by WhiteNoise
- Simpler architecture
- One deployment point

## 🎯 Next Steps

1. **If you want static site only**: Current setup works!
2. **If you want full Django app**: Deploy to Railway instead
3. **If you want hybrid**: Configure Railway backend URL in Firebase rewrites

## 📝 Firebase Configuration

Current `firebase.json`:
```json
{
  "hosting": {
    "public": "staticfiles",
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

This serves static files and redirects all routes to `index.html`.

