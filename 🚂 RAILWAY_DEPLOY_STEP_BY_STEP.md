# 🚂 Railway Deployment - Step by Step Guide

## 📋 Prerequisites Checklist

Before starting, make sure:
- ✅ Your code is pushed to GitHub (already done!)
- ✅ You have a GitHub account
- ✅ You have a Railway account (or can create one)

## 🚀 Step-by-Step Deployment

### STEP 1: Go to Railway

1. Open your web browser
2. Go to: **https://railway.app**
3. Click **"Login"** or **"Start a New Project"**

### STEP 2: Sign In / Sign Up

**If you don't have a Railway account:**
1. Click **"Sign Up"**
2. Choose **"Continue with GitHub"**
3. Authorize Railway to access your GitHub account

**If you already have an account:**
1. Click **"Login"**
2. Sign in with GitHub

### STEP 3: Create New Project

1. Once logged in, you'll see the Railway dashboard
2. Click the **"+ New Project"** button (usually in the top right or center)
3. You'll see options:
   - **"Deploy from GitHub repo"** ← Click this one!
   - "Empty Project"
   - "Deploy from Template"

### STEP 4: Connect GitHub Repository

1. Railway will show a list of your GitHub repositories
2. Find and click on: **`Shiku-beauty_hub`** (or `kangethe212/Shiku-beauty_hub`)
3. Railway will ask for permissions - click **"Authorize"** if needed
4. Click **"Deploy Now"** or **"Add Service"**

### STEP 5: Railway Auto-Detection

Railway will automatically:
- ✅ Detect it's a Python/Django project
- ✅ Find `requirements.txt`
- ✅ Find `Procfile`
- ✅ Start building your app

**You'll see:**
- Build logs in real-time
- Installation progress
- "Building..." status

### STEP 6: Add PostgreSQL Database

**While your app is building:**

1. In your Railway project dashboard, click **"+ New"** button
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will automatically:
   - Create a PostgreSQL database
   - Set `DATABASE_URL` environment variable
   - Link it to your Django service

### STEP 7: Wait for Deployment

Railway will automatically:
1. Install Python dependencies
2. Run `python manage.py collectstatic`
3. Run database migrations
4. Start Gunicorn server
5. Generate a public URL

**This takes 2-5 minutes**

### STEP 8: Get Your URL

Once deployment is complete:
1. Click on your service (the Django app)
2. Go to **"Settings"** tab
3. Find **"Generate Domain"** button
4. Click it to get your public URL

**Your site will be live at:**
- `https://your-app-name.railway.app`

### STEP 9: Create Admin User

**Option A: Using Railway Web Terminal**
1. In Railway dashboard, click on your service
2. Go to **"Deployments"** tab
3. Click on the latest deployment
4. Click **"View Logs"** or **"Open Terminal"**
5. Run:
   ```bash
   python manage.py createsuperuser
   ```
6. Follow prompts to create admin account

**Option B: Using Railway CLI**
```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Create superuser
railway run python manage.py createsuperuser
```

### STEP 10: Access Your Site!

1. **Main Website**: `https://your-app-name.railway.app`
2. **Admin Panel**: `https://your-app-name.railway.app/admin/`

## 🎯 What You'll See

### During Build:
```
[1/5] Installing Python 3.11...
[2/5] Installing dependencies from requirements.txt...
[3/5] Collecting static files...
[4/5] Running migrations...
[5/5] Starting Gunicorn...
✅ Deployment successful!
```

### After Deployment:
- ✅ Green "Active" status
- ✅ Public URL generated
- ✅ Database connected
- ✅ All services running

## ⚙️ Optional: Environment Variables

You can add these in Railway dashboard → Settings → Variables:

- `SECRET_KEY` - Generate a new one for production
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Railway auto-sets this, but you can add custom domains

## 🔍 Troubleshooting

### Issue: Build fails
- Check Railway logs for error messages
- Verify `requirements.txt` has all dependencies
- Ensure `Procfile` uses correct project name

### Issue: Database connection error
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is set automatically
- Try redeploying

### Issue: Static files not loading
- WhiteNoise is configured, should work automatically
- Check Railway logs for collectstatic errors
- Verify `STATIC_ROOT` setting

### Issue: 500 Error
- Check Railway logs
- Verify database migrations ran
- Check environment variables

## 📊 Monitoring

Railway dashboard shows:
- **Metrics**: CPU, Memory usage
- **Logs**: Real-time application logs
- **Deployments**: Deployment history
- **Settings**: Environment variables, domains

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Status shows "Active" (green)
- ✅ You can visit your URL
- ✅ Pages load correctly
- ✅ Admin panel accessible
- ✅ Static files (CSS, JS) load

## 🔄 Auto-Deploy

Once connected:
- Every push to `main` branch = automatic deployment
- Railway watches your GitHub repo
- Deploys changes automatically

## 📝 Next Steps After Deployment

1. ✅ Test all pages work
2. ✅ Create admin user
3. ✅ Add some test data
4. ✅ Verify static files load
5. ✅ Set up custom domain (optional)

## 🆘 Need Help?

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Check Logs**: Railway dashboard → Your service → Logs

---

## 🎯 Quick Summary

1. Go to **railway.app** → Login with GitHub
2. Click **"+ New Project"** → **"Deploy from GitHub repo"**
3. Select **`Shiku-beauty_hub`** repository
4. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
5. Wait for deployment (2-5 minutes)
6. Get your URL from Settings
7. Create admin user
8. Visit your live site! 🎉

---

**Your code is ready on GitHub. Just follow these steps!** 🚀

