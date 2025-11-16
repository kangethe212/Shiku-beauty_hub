# 🚂 Deploy Full Django App to Railway

## ✅ Pre-Deployment Checklist

Your project is already configured for Railway! Here's what's ready:

- ✅ `Procfile` - Gunicorn command configured
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - All dependencies included
- ✅ `settings.py` - Database and static files configured
- ✅ WhiteNoise - Static file serving enabled
- ✅ Database - PostgreSQL auto-configured by Railway

## 🚀 Deployment Steps

### Step 1: Push Code to GitHub

Make sure all changes are committed and pushed:

```bash
git add -A
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Connect Railway to GitHub

1. Go to **https://railway.app**
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `Shiku-beauty_hub`
5. Railway will automatically detect Django

### Step 3: Add PostgreSQL Database

1. In Railway dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically sets `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables (Optional)

Railway will auto-detect most settings, but you can add:

- `SECRET_KEY` - Django secret key (generate one)
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Railway auto-sets this

### Step 5: Deploy!

Railway will automatically:
- ✅ Detect Python/Django
- ✅ Install dependencies from `requirements.txt`
- ✅ Run migrations automatically
- ✅ Start Gunicorn using `Procfile`
- ✅ Serve static files with WhiteNoise
- ✅ Generate public URL

## 📋 What Railway Does Automatically

1. **Detects Django** - Recognizes `manage.py` and `settings.py`
2. **Installs Dependencies** - Runs `pip install -r requirements.txt`
3. **Collects Static Files** - Runs `collectstatic` automatically
4. **Runs Migrations** - Executes database migrations
5. **Starts Server** - Uses `Procfile` or `railway.json` startCommand
6. **Creates Database** - PostgreSQL with `DATABASE_URL` set
7. **Generates URL** - Creates public `.railway.app` domain

## 🎯 Your App Will Be Live At:

After deployment, Railway will provide:
- **Public URL**: `https://your-app-name.railway.app`
- **Admin Panel**: `https://your-app-name.railway.app/admin/`

## 🔧 Configuration Files

### Procfile
```
web: gunicorn her_beauty_hub.wsgi:application --bind 0.0.0.0:$PORT
```

### railway.json
```json
{
  "deploy": {
    "startCommand": "gunicorn her_beauty_hub.wsgi:application --bind 0.0.0.0:$PORT"
  }
}
```

### settings.py (Already Configured)
- ✅ Database: Auto-detects `DATABASE_URL`
- ✅ Static Files: WhiteNoise enabled
- ✅ Allowed Hosts: `.railway.app` included
- ✅ CSRF Origins: Railway domains included

## 📝 Post-Deployment Steps

### 1. Create Admin User

After deployment, run:

```bash
railway run python manage.py createsuperuser
```

Or use Railway's CLI:
```bash
railway login
railway link
railway run python manage.py createsuperuser
```

### 2. Verify Deployment

- ✅ Visit your Railway URL
- ✅ Check admin panel works
- ✅ Verify static files load (CSS, JS, images)
- ✅ Test a few pages

### 3. Set Custom Domain (Optional)

1. Go to Railway project settings
2. Click **"Settings"** → **"Networking"**
3. Add your custom domain

## 🎉 Benefits of Railway Deployment

- ✅ **Free Tier Available** - $5 free credit monthly
- ✅ **Auto-Deploy** - Deploys on every git push
- ✅ **PostgreSQL Included** - Database auto-configured
- ✅ **HTTPS by Default** - SSL certificates included
- ✅ **Easy Scaling** - Upgrade when needed
- ✅ **Simple Setup** - Just connect GitHub repo

## 🆘 Troubleshooting

### Issue: App crashes on startup
- Check `Procfile` uses correct project name
- Verify `requirements.txt` has all dependencies
- Check Railway logs for errors

### Issue: Static files not loading
- WhiteNoise is configured in `settings.py`
- Run `collectstatic` manually if needed
- Check `STATIC_ROOT` setting

### Issue: Database connection error
- Railway auto-sets `DATABASE_URL`
- Verify PostgreSQL service is running
- Check database migrations ran

## 📚 Useful Links

- **Railway Dashboard**: https://railway.app
- **Railway Docs**: https://docs.railway.app
- **Your GitHub Repo**: https://github.com/kangethe212/Shiku-beauty_hub

## 🎯 Quick Deploy Command

Once connected to Railway, every push to `main` branch auto-deploys!

```bash
git push origin main
```

That's it! Railway handles the rest! 🚀

