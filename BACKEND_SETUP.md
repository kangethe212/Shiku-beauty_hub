# 🚀 Django Backend Setup Guide - Her Beauty Hub

Complete guide to setting up the Django backend for dynamic content management.

---

## 📋 Overview

This backend integration allows the site owner to:
- ✅ Manage services dynamically through admin panel
- ✅ Upload and manage gallery images
- ✅ Track booking requests
- ✅ Manage contact form submissions
- ✅ Add/approve customer testimonials
- ✅ Manage products (fashion, perfumes, beauty items)

---

## 🗂️ Project Structure

```
her_beauty_hub/
├── manage.py
├── her_beauty_hub/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── beautyhub/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── apps.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── services.html
│   ├── gallery.html
│   ├── contact.html
│   └── booking.html
├── media/
│   ├── services/
│   ├── products/
│   └── gallery/
└── static/
```

---

## 🔧 Installation Steps

### Step 1: Install Dependencies

```bash
# Install Django and Pillow (for image handling)
pip install Django>=4.2 Pillow>=10.0.0

# Or install from requirements.txt
pip install -r requirements.txt
```

### Step 2: Create Database Tables

```bash
# Make migrations for beautyhub app
python manage.py makemigrations beautyhub

# Apply migrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, beautyhub
Running migrations:
  Applying beautyhub.0001_initial... OK
```

### Step 3: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin` (or your preferred username)
- Email: `admin@herbeautyhub.com`
- Password: (choose a strong password)

### Step 4: Create Media Folders

```bash
# Windows
mkdir media
mkdir media\services
mkdir media\products
mkdir media\gallery

# Linux/Mac
mkdir -p media/{services,products,gallery}
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 🎛️ Admin Panel Setup

### Access Admin Panel

1. Navigate to: **http://127.0.0.1:8000/admin/**
2. Log in with the superuser credentials you created
3. You'll see the Her Beauty Hub Administration panel

### Admin Dashboard Sections

The admin panel includes:

#### 1. **Services**
- Add/edit/delete beauty and fashion services
- Upload service images
- Set pricing and duration
- Mark services as featured (appears on home page)
- Set display order

#### 2. **Products**
- Manage fashion items, perfumes, and beauty products
- Categorize products
- Set prices and availability
- Mark as featured

#### 3. **Gallery Items**
- Upload portfolio images
- Add titles and descriptions
- Categorize by type (Hair, Makeup, Fashion, etc.)
- Mark featured items

#### 4. **Bookings**
- View all appointment requests
- Change status (Pending → Confirmed → Completed)
- Filter by date and service
- Search by client name or email

#### 5. **Contact Messages**
- Read all contact form submissions
- Mark as read/replied
- Search and filter messages

#### 6. **Testimonials**
- Add customer reviews
- Approve testimonials for display
- Feature on home page
- Assign to specific services

---

## 📝 Adding Initial Content

### Add Services

1. Go to Admin → Services → Add Service
2. Fill in:
   - **Name**: Hair Styling
   - **Description**: Expert hair styling for every occasion...
   - **Icon Class**: fa-cut
   - **Price**: 30.00
   - **Duration**: 1-2 hours
   - **Featured**: ✓ (Yes)
   - **Active**: ✓ (Yes)
   - **Order**: 1
3. Click "Save"

Repeat for all services:
- Hair Treatment (fa-spa, $25, featured)
- Clothing & Fashion (fa-tshirt, featured)
- Perfume Sales (fa-spray-can, $20, featured)
- Make-up & Beauty Care (fa-palette, $35, featured)
- Beauty Consultation (fa-comments, Free, featured)

### Add Gallery Images

1. Go to Admin → Gallery Items → Add Gallery Item
2. Fill in:
   - **Title**: Gorgeous Braided Style
   - **Description**: Beautiful braided crown for special occasions
   - **Image**: Upload an image file
   - **Category**: Hair
   - **Featured**: ✓ (optional)
3. Click "Save"

Add at least 8-12 gallery items for a full display.

### Add Testimonials

1. Go to Admin → Testimonials → Add Testimonial
2. Fill in:
   - **Client Name**: Amara Johnson
   - **Client Initial**: A (auto-filled)
   - **Rating**: 5
   - **Testimonial**: "The hair treatment was amazing! My hair has never felt so healthy..."
   - **Service**: Select a service (optional)
   - **Approved**: ✓ (Yes, to show on website)
   - **Featured**: ✓ (Yes, to show on home page)
3. Click "Save"

Add at least 3 testimonials for the home page.

---

## 🔍 Testing the Website

### Test Home Page
- Visit http://127.0.0.1:8000/
- Should see featured services (if added)
- Should see testimonials (if added and approved)

### Test Services Page
- Visit http://127.0.0.1:8000/services/
- Should display all active services from database
- Images should load (if uploaded)

### Test Gallery Page
- Visit http://127.0.0.1:8000/gallery/
- Should show all uploaded gallery images
- Click images for lightbox view

### Test Contact Form
- Visit http://127.0.0.1:8000/contact/
- Fill and submit the form
- Check Admin → Contact Messages
- Should see new submission

### Test Booking Form
- Visit http://127.0.0.1:8000/booking/
- Fill out appointment request
- Check Admin → Bookings
- Should see new booking request

---

## 📧 Email Configuration (Optional)

### Development (Console Email)
Already configured! Emails print to console.

### Production (Gmail SMTP)

Edit `her_beauty_hub/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
DEFAULT_FROM_EMAIL = 'Her Beauty Hub <your-email@gmail.com>'
ADMIN_EMAIL = 'your-admin-email@gmail.com'
```

**Important**: For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Generate an "App Password" (Google Account → Security → App Passwords)
3. Use the App Password in settings (not your regular password)

---

## 🎨 Customizing Models

### Add Fields to Existing Models

1. Edit `beautyhub/models.py`
2. Add new field, e.g.:
   ```python
   class Service(models.Model):
       # ... existing fields ...
       discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Create New Model

1. Add model in `beautyhub/models.py`
2. Register in `beautyhub/admin.py`
3. Run migrations
4. Access in admin panel

---

## 🔐 Security Checklist

### For Production:

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up static files collection
- [ ] Configure CORS if needed
- [ ] Add rate limiting
- [ ] Enable CSRF protection (already done)

---

## 📊 Database Models Reference

### Service Model
- `name`: Service name (CharField)
- `description`: Detailed description (TextField)
- `image`: Service image (ImageField, optional)
- `price`: Starting price (DecimalField, optional)
- `duration`: Service duration (CharField)
- `icon_class`: Font Awesome icon (CharField)
- `featured`: Show on home page (BooleanField)
- `active`: Currently available (BooleanField)
- `order`: Display order (IntegerField)

### Product Model
- `name`: Product name
- `description`: Product description
- `category`: fashion/perfume/beauty/accessories
- `image`: Product image
- `price`: Product price
- `available`: In stock status
- `featured`: Featured on home page

### GalleryItem Model
- `title`: Image title
- `description`: Image description
- `image`: Gallery image file
- `category`: Category/tag
- `featured`: Featured item
- `uploaded_at`: Upload timestamp

### Booking Model
- `name`: Client name
- `email`: Client email
- `phone`: Contact number
- `service`: Selected service (ForeignKey)
- `date`: Preferred date
- `time`: Preferred time
- `message`: Additional notes
- `status`: pending/confirmed/cancelled/completed

### ContactMessage Model
- `name`: Sender name
- `email`: Sender email
- `phone`: Phone number
- `subject`: Message subject
- `message`: Message content
- `status`: new/read/replied

### Testimonial Model
- `client_name`: Customer name
- `client_initial`: First letter (for avatar)
- `rating`: 1-5 stars
- `testimonial`: Review text
- `service`: Related service
- `approved`: Show on website
- `featured`: Show on home page

---

## 🛠️ Common Tasks

### Backup Database

```bash
# Backup SQLite database
python manage.py dumpdata > backup.json

# Or copy the db file
copy db.sqlite3 backup_db.sqlite3
```

### Restore Database

```bash
python manage.py loaddata backup.json
```

### Clear All Data

```bash
python manage.py flush
```

### Create Sample Data (Optional)

Create `beautyhub/management/commands/load_sample_data.py` for quick testing.

---

## 🐛 Troubleshooting

### "No such table" Error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Images Not Displaying
**Solution**: Check media settings and ensure folders exist
```bash
mkdir media media\services media\products media\gallery
```

### Admin CSS Not Loading
**Solution**: Run collectstatic
```bash
python manage.py collectstatic
```

### Form Not Submitting
**Solution**: Check CSRF token is present and DEBUG is True

### "Module not found" Error
**Solution**: Install missing package
```bash
pip install Pillow
```

---

## 📱 Mobile Testing

Test on actual devices:
1. Find your local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Update `ALLOWED_HOSTS` in settings.py:
   ```python
   ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.X']
   ```
3. Run server: `python manage.py runserver 0.0.0.0:8000`
4. Access from mobile: `http://192.168.1.X:8000`

---

## 🚀 Deployment

### Deploy to PythonAnywhere

1. Create account at pythonanywhere.com
2. Upload files via Git or file manager
3. Create virtual environment
4. Configure WSGI file
5. Set static files mapping
6. Reload web app

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku login
heroku create her-beauty-hub
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to DigitalOcean/AWS

1. Set up server with Ubuntu
2. Install Python, pip, PostgreSQL
3. Clone repository
4. Configure Gunicorn + Nginx
5. Set up SSL with Let's Encrypt
6. Configure environment variables

---

## 📚 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Pillow Documentation**: https://pillow.readthedocs.io/
- **Django Admin Cookbook**: https://books.agiliq.com/projects/django-admin-cookbook/
- **Two Scoops of Django**: Best practices book

---

## ✅ Success Checklist

After setup, you should have:

- [x] Django project running
- [x] All migrations applied
- [x] Superuser account created
- [x] Admin panel accessible
- [x] Media folders created
- [x] At least 3-6 services added
- [x] At least 6-12 gallery images uploaded
- [x] At least 3 testimonials added
- [x] Contact form working
- [x] Booking form working
- [x] All pages displaying correctly

---

## 💡 Pro Tips

1. **Regular Backups**: Back up your database weekly
2. **Image Optimization**: Compress images before uploading
3. **Consistent Naming**: Use clear, descriptive names
4. **Test Everything**: Test all forms and features after changes
5. **Version Control**: Use Git to track changes
6. **Documentation**: Document any customizations you make

---

## 🎯 Next Steps

1. ✅ Complete initial setup
2. ✅ Add your business content
3. ✅ Customize colors/branding
4. ⬜ Add real photos to gallery
5. ⬜ Configure production email
6. ⬜ Set up analytics
7. ⬜ Deploy to production
8. ⬜ Launch and promote! 🎉

---

**Need Help?** Check the Django documentation or the project README.md

**Happy Building! 💕**

