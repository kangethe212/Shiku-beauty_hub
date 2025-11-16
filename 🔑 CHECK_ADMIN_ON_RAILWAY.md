# 🔑 Check/Create Admin User on Railway

## 📋 Current Status

**Local Database** (your computer):
- ✅ Admin user exists: `admin` (admin@herbeautyhub.com)

**Railway Database** (production):
- ❓ Need to check/create admin user separately

**Important**: Railway uses a separate PostgreSQL database, so you need to create the admin user on Railway even if one exists locally.

---

## 🔍 Check Admin Users on Railway

### Method 1: Using Railway Web Terminal

1. Go to **Railway Dashboard**: https://railway.app
2. Click on your **Django service**
3. Go to **"Deployments"** tab
4. Click on **latest deployment**
5. Click **"View Logs"** or **"Open Terminal"**
6. Run this command:
   ```bash
   python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); admins = User.objects.filter(is_superuser=True); print('Admin users:', admins.count()); [print(f'Username: {u.username}, Email: {u.email}') for u in admins]"
   ```

### Method 2: Using Railway CLI

```bash
railway run python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Admins:', User.objects.filter(is_superuser=True).count())"
```

---

## 🚀 Create Admin User on Railway

### If No Admin User Exists:

**Using Railway Web Terminal:**
1. Railway Dashboard → Your service → Deployments → Latest → Terminal
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter:
   - **Username**: `admin` (or your choice)
   - **Email**: `bennymaish01@gmail.com` (or your email)
   - **Password**: (create a strong password)
   - **Password (again)**: (confirm)

**Using Railway CLI:**
```bash
railway run python manage.py createsuperuser
```

---

## 🔄 Reset Admin Password on Railway

If you forgot the password:

**Method 1: Change Password Command**
```bash
railway run python manage.py changepassword admin
```

**Method 2: Django Shell**
```bash
railway run python manage.py shell
```
Then in the shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='admin')
user.set_password('your_new_password')
user.save()
exit()
```

---

## 🎯 Quick Steps

1. **Go to Railway Dashboard**
2. **Click your service** → **Deployments** → **Latest**
3. **Open Terminal**
4. **Check existing admins**:
   ```bash
   python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print([u.username for u in User.objects.filter(is_superuser=True)])"
   ```
5. **If no admin exists, create one**:
   ```bash
   python manage.py createsuperuser
   ```

---

## 🔐 Password Security

**Django passwords are hashed** - you cannot "check" or "view" them. You can only:
- ✅ Create a new admin user
- ✅ Reset an existing password
- ✅ Change an existing password

---

## ✅ After Creating Admin

1. Visit: `https://your-app.railway.app/admin/`
2. Login with:
   - **Username**: (what you entered)
   - **Password**: (what you entered)
3. You should see the Django admin dashboard

---

## 📝 Recommended Admin Credentials

**Username**: `admin`
**Email**: `bennymaish01@gmail.com`
**Password**: (create a strong, unique password)

**Store your password securely!** 🔐

---

## 🆘 Troubleshooting

### "No such user"
→ Create admin with `createsuperuser`

### "Invalid password"
→ Reset password with `changepassword`

### Can't access terminal
→ Use Railway CLI instead

### "Command not found"
→ Make sure you're in Railway terminal, not local

---

**Remember**: Railway database is separate from local - you need to create admin on Railway! 🚀

