# 🔧 Fix Server Error (500) on Railway

## 🚨 Common Causes of 500 Errors

### 1. Database Migrations Not Run
**Most Common Issue!**

Railway might not have run migrations automatically.

**Fix:**
```bash
# In Railway terminal or CLI
railway run python manage.py migrate
```

### 2. Missing SECRET_KEY
Django needs a SECRET_KEY in production.

**Fix:**
1. Generate a new secret key:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. Add to Railway environment variables:
   - Go to Railway dashboard
   - Settings → Variables
   - Add: `SECRET_KEY` = (generated key)

### 3. DEBUG Should Be False
In production, DEBUG should be False.

**Fix:**
Add to Railway environment variables:
- `DEBUG` = `False`

### 4. Static Files Not Collected
Static files might not be collected.

**Fix:**
```bash
railway run python manage.py collectstatic --noinput
```

### 5. Database Connection Issue
PostgreSQL might not be connected properly.

**Fix:**
- Verify PostgreSQL service is running in Railway
- Check DATABASE_URL is set automatically
- Try redeploying

---

## 🔍 How to Debug

### Step 1: Check Railway Logs

1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on latest deployment
5. View "Logs" tab
6. Look for error messages

### Step 2: Common Error Messages

**"No such table" or "relation does not exist"**
→ Run migrations: `railway run python manage.py migrate`

**"SECRET_KEY" error**
→ Add SECRET_KEY to environment variables

**"Static files" error**
→ Run collectstatic: `railway run python manage.py collectstatic --noinput`

**"Database connection" error**
→ Check PostgreSQL service is running

---

## 🛠️ Quick Fix Steps

### Option 1: Using Railway Web Terminal

1. Go to Railway dashboard
2. Click on your service
3. Click "Deployments" → Latest deployment
4. Click "View Logs" or "Open Terminal"
5. Run these commands:

```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check for errors
python manage.py check --deploy
```

### Option 2: Using Railway CLI

```bash
# Login
railway login

# Link to project
railway link

# Run migrations
railway run python manage.py migrate

# Collect static files
railway run python manage.py collectstatic --noinput

# Check deployment
railway run python manage.py check --deploy
```

---

## ⚙️ Environment Variables to Add

In Railway dashboard → Settings → Variables:

1. **SECRET_KEY** (Required)
   - Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Add the generated key

2. **DEBUG** (Recommended)
   - Set to: `False`

3. **ALLOWED_HOSTS** (Optional)
   - Railway auto-sets this, but you can add your domain

---

## 🔄 Redeploy After Fixes

After making changes:
1. Railway will auto-redeploy if you push to GitHub
2. Or manually trigger redeploy in Railway dashboard
3. Check logs to verify it's working

---

## 📋 Step-by-Step Fix

1. **Check Logs First**
   - Railway dashboard → Your service → Logs
   - Look for the actual error message

2. **Run Migrations**
   ```bash
   railway run python manage.py migrate
   ```

3. **Add SECRET_KEY**
   - Generate one
   - Add to Railway environment variables

4. **Set DEBUG=False**
   - Add to Railway environment variables

5. **Collect Static Files**
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

6. **Redeploy**
   - Trigger new deployment
   - Check if error is fixed

---

## 🎯 Most Likely Fix

**90% of 500 errors are caused by:**
1. Missing migrations → Run `migrate`
2. Missing SECRET_KEY → Add to environment variables

Try these first!

---

## 🆘 Still Not Working?

1. **Check Railway Logs** - Look for specific error
2. **Check Database** - Verify PostgreSQL is running
3. **Check Settings** - Verify environment variables
4. **Contact Support** - Railway Discord or docs

---

## ✅ Verification

After fixes, verify:
- ✅ Site loads without 500 error
- ✅ Admin panel accessible
- ✅ Static files load (CSS, JS, images)
- ✅ Database queries work

---

**Start with running migrations - that's usually the issue!** 🚀

