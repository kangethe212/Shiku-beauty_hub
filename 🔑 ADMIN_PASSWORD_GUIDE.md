# 🔑 Admin Password Guide

## 📋 Admin User Status

Django doesn't store passwords in plain text - they're encrypted (hashed). You can't "check" a password, but you can:

1. **Create a new admin user** (if none exists)
2. **Reset an existing admin password**
3. **List existing admin users**

---

## 🚀 Create Admin User on Railway

### Option 1: Using Railway Web Terminal (Easiest)

1. Go to **Railway Dashboard**: https://railway.app
2. Click on your **Django service**
3. Go to **"Deployments"** tab
4. Click on **latest deployment**
5. Click **"View Logs"** or **"Open Terminal"**
6. Run this command:
   ```bash
   python manage.py createsuperuser
   ```
7. Follow the prompts:
   - Username: (enter your desired username)
   - Email: (enter your email)
   - Password: (enter a strong password)
   - Password (again): (confirm password)

### Option 2: Using Railway CLI

```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Create superuser
railway run python manage.py createsuperuser
```

---

## 🔄 Reset Admin Password

If you forgot your password, you can reset it:

### Method 1: Change Password Command

```bash
# On Railway terminal or CLI
python manage.py changepassword <username>
```

Replace `<username>` with your admin username.

### Method 2: Django Shell

```bash
# Open Django shell
python manage.py shell

# Then run:
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='your_username')
user.set_password('new_password')
user.save()
exit()
```

---

## 👥 List Existing Admin Users

To see if any admin users exist:

```bash
# On Railway terminal
python manage.py shell

# Then run:
from django.contrib.auth import get_user_model
User = get_user_model()
admins = User.objects.filter(is_superuser=True)
for admin in admins:
    print(f"Username: {admin.username}, Email: {admin.email}")
exit()
```

---

## 🔍 Check if Admin User Exists

### Quick Check Script

```bash
# On Railway terminal
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Admin users:', User.objects.filter(is_superuser=True).count())"
```

---

## 🎯 Quick Steps to Create Admin

1. **Go to Railway Dashboard**
2. **Click your service** → **Deployments** → **Latest deployment**
3. **Open Terminal/Logs**
4. **Run**: `python manage.py createsuperuser`
5. **Enter details** when prompted
6. **Access admin**: `https://your-app.railway.app/admin/`

---

## 🔐 Password Requirements

Django admin passwords should be:
- At least 8 characters (recommended)
- Not too common
- Mix of letters, numbers, and symbols (recommended)

---

## 🆘 Troubleshooting

### "Command not found"
- Make sure you're in the Railway terminal
- Verify you're in the correct directory

### "No such user"
- User doesn't exist - create one with `createsuperuser`

### "Permission denied"
- Make sure you're using Railway's terminal, not local terminal

### Can't access admin panel
- Verify admin user was created successfully
- Check username/password are correct
- Make sure you're using the right URL: `/admin/`

---

## 📝 Recommended Admin Setup

**Username**: `admin` (or your preferred name)
**Email**: Your email address
**Password**: Strong, unique password

**Example**:
```
Username: admin
Email: bennymaish01@gmail.com
Password: [create a strong password]
```

---

## ✅ Verification

After creating admin user:

1. Visit: `https://your-app.railway.app/admin/`
2. Login with your username and password
3. You should see the Django admin dashboard

---

## 🔄 Create Admin via Script (Alternative)

If you want to automate it, you can create a script:

```python
# create_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'bennymaish01@gmail.com', 'your_password')
    print("Admin user created!")
else:
    print("Admin user already exists!")
```

Then run: `python create_admin.py`

---

**Remember**: Django passwords are hashed - you can't "check" them, only reset or create new ones! 🔐

