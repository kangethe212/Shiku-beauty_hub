# 🚀 Quick Start Guide - Her Beauty Hub

Get your website up and running in minutes!

---

## ⚡ Fast Setup (5 Minutes)

### Step 1: Create Django Project
```bash
# Navigate to your desired directory
cd "c:\shiku salon"

# Create Django project
django-admin startproject herbeautyhub .

# Create a Django app
python manage.py startapp main
```

### Step 2: Configure Settings
Edit `herbeautyhub/settings.py`:

```python
# Add 'main' to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # ← Add this
]

# Update TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Add this
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Step 3: Copy Views and URLs
```bash
# Copy the views.py file to your app
copy views.py main\views.py

# Copy the urls.py file to your app
copy urls.py main\urls.py
```

### Step 4: Update Project URLs
Edit `herbeautyhub/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # ← Add this
]
```

### Step 5: Run the Server
```bash
# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

### Step 6: Open Your Browser
Visit: **http://127.0.0.1:8000/**

---

## 🎨 You Should See:

✅ **Home Page** - Beautiful hero section with gradient background  
✅ **Navigation** - Working navbar with all links  
✅ **Mobile Menu** - Responsive hamburger menu  
✅ **All Pages** - Home, About, Services, Gallery, Contact  
✅ **Footer** - Social media links and contact info  

---

## 📝 Next Steps

### 1. **Customize Content**
- Edit text in the templates to match your business
- Update phone numbers, email, and social media links
- Change business hours in contact.html

### 2. **Add Your Branding**
- Replace "Her Beauty Hub" with your business name
- Add your logo image
- Customize colors if needed

### 3. **Set Up Admin Panel**
```bash
# Create superuser
python manage.py createsuperuser

# Visit admin panel at http://127.0.0.1:8000/admin/
```

### 4. **Add Real Images**
- Create `static` folder structure:
  ```
  static/
    └── images/
        ├── logo.png
        ├── gallery/
        └── services/
  ```
- Update settings.py:
  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [BASE_DIR / 'static']
  ```

### 5. **Make Contact Form Functional**
- Add email backend in settings.py
- Or save submissions to database (create a model)
- Add reCAPTCHA for spam protection

---

## 🐛 Common Issues

### Issue: "TemplateDoesNotExist"
**Solution**: Make sure `'DIRS': [BASE_DIR / 'templates']` is in settings.py

### Issue: "NoReverseMatch"
**Solution**: Check that url names in templates match those in urls.py

### Issue: "Static files not loading"
**Solution**: Make sure you're using `{% load static %}` in templates

### Issue: "CSRF token missing"
**Solution**: The `{% csrf_token %}` tag is already in the contact form

---

## 📱 Test Responsiveness

1. **Open Developer Tools** (F12)
2. **Toggle device toolbar** (Ctrl + Shift + M)
3. **Test different screen sizes**:
   - Mobile: 375px
   - Tablet: 768px
   - Desktop: 1440px

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Change `DEBUG = False` in settings.py
- [ ] Set `ALLOWED_HOSTS` in settings.py
- [ ] Configure static files for production
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Add SSL certificate (HTTPS)
- [ ] Set up email backend
- [ ] Add Google Analytics
- [ ] Create privacy policy and terms pages
- [ ] Test all forms and links
- [ ] Optimize images
- [ ] Set up backups

---

## 🌐 Deployment Options

### Option 1: PythonAnywhere (Free)
- Good for beginners
- Free tier available
- Easy Django deployment

### Option 2: Heroku
- Popular choice
- Git-based deployment
- Free tier available

### Option 3: DigitalOcean
- More control
- Affordable
- Requires more setup

### Option 4: Railway
- Modern platform
- Easy deployment
- Free tier available

---

## 💡 Pro Tips

1. **Version Control**: Use Git to track changes
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Her Beauty Hub"
   ```

2. **Virtual Environment**: Always use a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Environment Variables**: Use python-decouple for secrets
   ```python
   # settings.py
   from decouple import config
   SECRET_KEY = config('SECRET_KEY')
   ```

4. **Regular Backups**: Back up your database regularly

5. **Keep Django Updated**: Stay on LTS (Long Term Support) versions

---

## 📞 Need Help?

- **Django Documentation**: https://docs.djangoproject.com/
- **Tailwind Documentation**: https://tailwindcss.com/docs
- **Stack Overflow**: Search for Django-related issues
- **Django Forum**: https://forum.djangoproject.com/

---

## ✅ Success Checklist

After completing setup, you should have:

- [x] All 6 pages working (Home, About, Services, Gallery, Contact)
- [x] Responsive design on all devices
- [x] Working navigation menu
- [x] Mobile hamburger menu
- [x] Contact form (ready for backend integration)
- [x] Beautiful UI with Tailwind CSS
- [x] Smooth animations and hover effects
- [x] Social media links in footer
- [x] Professional branding

---

**Congratulations! Your website is now live locally! 🎉**

*Ready to empower women through beauty, style, and confidence!*

