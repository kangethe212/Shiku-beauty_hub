# ⚡ Quick Backend Start - Her Beauty Hub

Ultra-fast setup guide in 5 minutes!

---

## 🚀 Quick Commands

```bash
# 1. Install dependencies
pip install Django Pillow

# 2. Create database
python manage.py makemigrations beautyhub
python manage.py migrate

# 3. Create admin account
python manage.py createsuperuser

# 4. Create media folders
mkdir media media\services media\products media\gallery

# 5. Run server
python manage.py runserver
```

---

## 🎯 Access Points

- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Contact Form**: http://127.0.0.1:8000/contact/
- **Booking Form**: http://127.0.0.1:8000/booking/
- **Services**: http://127.0.0.1:8000/services/
- **Gallery**: http://127.0.0.1:8000/gallery/

---

## 📝 First Steps in Admin

1. **Login** to admin panel with superuser credentials
2. **Add 3-6 Services**:
   - Hair Styling ($30, fa-cut, featured)
   - Hair Treatment ($25, fa-spa, featured)
   - Clothing & Fashion (fa-tshirt, featured)
   - Perfume Sales ($20, fa-spray-can)
   - Makeup & Beauty ($35, fa-palette)
   - Beauty Consultation (Free, fa-comments)

3. **Upload 6-12 Gallery Images**:
   - Add titles and categories
   - Mark some as featured

4. **Add 3 Testimonials**:
   - Name, rating, review text
   - Approve and feature them

5. **Test Forms**:
   - Submit contact form
   - Create booking request
   - Check admin for submissions

---

## ✅ Verify Everything Works

- [ ] Home page shows featured services
- [ ] Home page shows testimonials
- [ ] Services page displays all services
- [ ] Gallery shows uploaded images
- [ ] Contact form submits successfully
- [ ] Booking form submits successfully
- [ ] Admin panel shows all submissions

---

## 🎨 Customize

### Update Business Info
- Edit footer in `templates/base.html`
- Update phone/email/address
- Change social media links

### Change Colors
- Edit CSS variables in `templates/base.html`
- Update color scheme throughout

### Add Your Logo
- Replace text logo in navbar with image

---

## 📱 Test on Mobile

```bash
# Find your IP address
ipconfig  # Windows
ifconfig  # Mac/Linux

# Update settings.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'YOUR_IP_HERE']

# Run server
python manage.py runserver 0.0.0.0:8000

# Access from phone
http://YOUR_IP:8000
```

---

## 🐛 Quick Fixes

### Database Error?
```bash
python manage.py migrate
```

### Images Not Showing?
```bash
mkdir media media\services media\products media\gallery
```

### Form Not Working?
- Check CSRF token is in form
- Verify DEBUG = True in settings.py

### Admin CSS Broken?
```bash
python manage.py collectstatic
```

---

## 📦 Database Models

### Service
- Name, description, image, price, duration, icon
- Featured, active, order

### Gallery Item
- Title, description, image, category
- Featured, uploaded_at

### Booking
- Name, email, phone, service, date, time
- Message, status (pending/confirmed/completed)

### Contact Message
- Name, email, phone, subject, message
- Status (new/read/replied)

### Testimonial
- Client name, rating, testimonial, service
- Approved, featured

### Product
- Name, description, category, image, price
- Available, featured

---

## 🎯 Admin Actions

### Services
- ✏️ Add/Edit/Delete
- 🖼️ Upload images
- ⭐ Mark as featured
- ✅ Set active/inactive
- 🔢 Set display order

### Bookings
- 👀 View all requests
- ✅ Mark as confirmed
- ✔️ Mark as completed
- ❌ Mark as cancelled

### Contact Messages
- 📧 Read messages
- ✅ Mark as read
- ↩️ Mark as replied

### Testimonials
- ✅ Approve for display
- ⭐ Feature on home page
- ✏️ Edit content

### Gallery
- 🖼️ Upload images
- 📝 Add titles/descriptions
- 🏷️ Categorize
- ⭐ Mark as featured

---

## 💡 Pro Tips

1. **Compress images** before uploading (< 500KB recommended)
2. **Use descriptive filenames** for images
3. **Fill all fields** in admin for best results
4. **Test forms** after every change
5. **Backup database** regularly:
   ```bash
   python manage.py dumpdata > backup.json
   ```

---

## 🚀 Deploy

### PythonAnywhere (Free)
1. Create account
2. Upload files
3. Configure WSGI
4. Done!

### Heroku
```bash
heroku create her-beauty-hub
git push heroku main
heroku run python manage.py migrate
```

---

## 📞 Need More Help?

- **Full Guide**: See BACKEND_SETUP.md
- **Django Docs**: https://docs.djangoproject.com/
- **Project README**: See README.md

---

**You're all set! 🎉**

*Time to make Her Beauty Hub shine! 💕✨*

