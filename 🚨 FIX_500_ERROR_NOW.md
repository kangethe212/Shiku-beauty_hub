# 🚨 Fix 500 Error - Quick Guide

## ⚡ Most Common Cause: Missing Migrations

**90% of 500 errors are because migrations weren't run!**

---

## 🔧 Quick Fix (2 Steps)

### Step 1: Run Migrations

**Using Railway Web Terminal:**
1. Go to Railway dashboard
2. Click on your service
3. Click "Deployments" → Latest deployment
4. Click "View Logs" or "Open Terminal"
5. Run:
   ```bash
   python manage.py migrate
   ```

**Using Railway CLI:**
```bash
railway run python manage.py migrate
```

### Step 2: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

Or with Railway CLI:
```bash
railway run python manage.py collectstatic --noinput
```

---

## 🔍 Check Railway Logs First

1. Railway dashboard → Your service
2. Click "Deployments" tab
3. Click latest deployment
4. View "Logs" tab
5. Look for the actual error message

**Common errors you might see:**
- "No such table" → Run migrations
- "relation does not exist" → Run migrations
- "SECRET_KEY" → Add to environment variables
- "Static files" → Run collectstatic

---

## ⚙️ Add Environment Variables

In Railway dashboard → Settings → Variables:

### 1. SECRET_KEY (Important!)
Generate one:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add to Railway:
- Key: `SECRET_KEY`
- Value: (paste generated key)

### 2. DEBUG
- Key: `DEBUG`
- Value: `False`

---

## 📋 Complete Fix Checklist

1. ✅ **Check Railway Logs** - See actual error
2. ✅ **Run Migrations** - `python manage.py migrate`
3. ✅ **Collect Static Files** - `python manage.py collectstatic --noinput`
4. ✅ **Add SECRET_KEY** - To environment variables
5. ✅ **Set DEBUG=False** - To environment variables
6. ✅ **Redeploy** - Trigger new deployment
7. ✅ **Test** - Visit your site

---

## 🎯 Try This First

**Most likely fix - run this:**

```bash
railway run python manage.py migrate
```

Then refresh your site. If still 500, check logs for the specific error.

---

## 🆘 Still Not Working?

1. **Check Railway Logs** - Look for specific error message
2. **Verify Database** - PostgreSQL service is running
3. **Check Environment Variables** - SECRET_KEY, DEBUG set
4. **Try Redeploying** - Trigger new deployment

---

**Start with migrations - that fixes 90% of 500 errors!** 🚀

