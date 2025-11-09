# Her Beauty Hub - Frontend Templates

A beautiful, modern, and responsive frontend for a beauty and fashion business website. Built with **Django Templates** and **Tailwind CSS**.

---

## 🌟 Features

- **Modern & Elegant Design**: Soft pink, gold, and beige color palette perfect for a feminine beauty brand
- **Fully Responsive**: Beautiful layouts on mobile, tablet, and desktop
- **Django Template Structure**: Uses template inheritance with `base.html`
- **Tailwind CSS Styling**: Utility-first CSS framework via CDN
- **Smooth Animations**: Hover effects, fade-ins, and transitions
- **Social Media Integration**: Instagram, TikTok, YouTube, and WhatsApp links
- **SEO-Friendly**: Proper heading structure and semantic HTML

---

## 📁 Project Structure

```
templates/
├── base.html          # Base template with navbar, footer, and common elements
├── index.html         # Home page with hero section and category cards
├── about.html         # About page with founder story and values
├── services.html      # Services page with 6 service cards
├── gallery.html       # Gallery page with image grid and lightbox
└── contact.html       # Contact page with form, map, and business hours
```

---

## 🎨 Design Theme

### Colors
- **Blush Pink**: `#f9c5d1`
- **Gold**: `#ffd700`
- **Beige**: `#fdf5e6`
- **White**: `#ffffff`

### Fonts
- **Headings**: Playfair Display (serif)
- **Body Text**: Inter (sans-serif)

### Typography
Google Fonts are loaded via CDN in `base.html`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.0+

### Installation

1. **Create a Django project** (if you haven't already):
   ```bash
   django-admin startproject herbeautyhub .
   ```

2. **Create a Django app**:
   ```bash
   python manage.py startapp main
   ```

3. **Configure settings.py**:
   ```python
   # settings.py
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'main',  # Your app name
   ]

   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [BASE_DIR / 'templates'],  # Point to templates folder
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

4. **Create views** in your app (`main/views.py`):
   ```python
   from django.shortcuts import render

   def index(request):
       return render(request, 'index.html')

   def about(request):
       return render(request, 'about.html')

   def services(request):
       return render(request, 'services.html')

   def gallery(request):
       return render(request, 'gallery.html')

   def contact(request):
       if request.method == 'POST':
           # Handle form submission here
           name = request.POST.get('name')
           email = request.POST.get('email')
           message = request.POST.get('message')
           # Add your form processing logic
           return render(request, 'contact.html', {'success': True})
       return render(request, 'contact.html')
   ```

5. **Configure URLs** (`main/urls.py`):
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.index, name='index'),
       path('about/', views.about, name='about'),
       path('services/', views.services, name='services'),
       path('gallery/', views.gallery, name='gallery'),
       path('contact/', views.contact, name='contact'),
   ]
   ```

6. **Include app URLs in project** (`herbeautyhub/urls.py`):
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('main.urls')),
   ]
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Visit your site**:
   Open your browser and go to `http://127.0.0.1:8000/`

---

## 📄 Page Descriptions

### 1. **Home Page** (`index.html`)
- Hero section with gradient background and call-to-action buttons
- 3-column category section (Hair & Beauty, Fashion, Perfumes)
- Testimonials section with client reviews
- Call-to-action section

### 2. **About Page** (`about.html`)
- Two-column layout with image and founder story
- Mission and vision cards
- Core values section
- Call-to-action buttons

### 3. **Services Page** (`services.html`)
- 3x2 grid of service cards:
  - Hair Styling
  - Hair Treatment
  - Clothing & Fashion
  - Perfume Sales
  - Make-up & Beauty Care
  - Beauty Consultation
- Why Choose Us section
- Business hours

### 4. **Gallery Page** (`gallery.html`)
- Responsive 12-image grid gallery
- Hover zoom effects
- Lightbox functionality (click to view larger)
- Social media integration

### 5. **Contact Page** (`contact.html`)
- Contact form with name, email, phone, service selection, and message
- Contact information cards (phone, email, location)
- Social media links
- Google Maps embed
- Quick contact buttons
- Business hours
- FAQ section

---

## 🎯 Customization Guide

### Change Colors
Update the color values in `base.html` under the `<style>` tag:
```css
:root {
    --blush-pink: #f9c5d1;  /* Change to your preferred pink */
    --gold: #ffd700;         /* Change to your preferred gold */
    --beige: #fdf5e6;        /* Change to your preferred beige */
}
```

### Add Your Logo
Replace the text logo in `base.html`:
```html
<!-- Find this in base.html navbar -->
<a href="{% url 'index' %}" class="text-2xl font-bold">
    Her Beauty Hub
</a>

<!-- Replace with an image: -->
<a href="{% url 'index' %}">
    <img src="{% static 'images/logo.png' %}" alt="Her Beauty Hub" class="h-10">
</a>
```

### Add Real Images
1. Create a `static` folder in your project
2. Add images to `static/images/`
3. Update Django settings to serve static files
4. Replace placeholder content in gallery and other pages

### Update Social Media Links
Find and update these in `base.html` footer and `contact.html`:
```html
<a href="https://instagram.com/yourusername" target="_blank">
<a href="https://wa.me/yourphonenumber" target="_blank">
```

### Update Contact Information
Edit `contact.html` and `base.html` footer:
- Phone number
- Email address
- Physical location
- Business hours

---

## 📱 Responsive Design

The templates are fully responsive with breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

Tailwind's responsive classes (`sm:`, `md:`, `lg:`) are used throughout.

---

## 🔌 Backend Integration

### To-Do for Full Integration:

1. **Set up Django Models** for:
   - Services
   - Gallery images
   - Testimonials
   - Contact form submissions

2. **Create an Admin Panel**:
   - Register models in `admin.py`
   - Use Django admin to manage content

3. **Add Form Handling**:
   - Process contact form submissions
   - Add email notifications
   - Store inquiries in database

4. **Add Static Files**:
   - Configure `STATIC_ROOT` and `MEDIA_ROOT`
   - Add real images for gallery
   - Add logo and favicon

5. **Implement SEO**:
   - Add meta tags
   - Create sitemap
   - Add Open Graph tags

6. **Add Security**:
   - Enable CSRF protection
   - Configure ALLOWED_HOSTS
   - Add reCAPTCHA to forms

---

## 🌐 External Resources Used

- **Tailwind CSS**: https://cdn.tailwindcss.com
- **Font Awesome**: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css
- **Google Fonts**: https://fonts.googleapis.com (Playfair Display & Inter)

---

## 📝 Notes

- All templates use Django template tags (`{% url %}`, `{% load static %}`, etc.)
- Form includes CSRF token for security
- Mobile menu toggle uses vanilla JavaScript (no jQuery needed)
- Gallery lightbox uses vanilla JavaScript
- All external links open in new tabs (`target="_blank"`)

---

## 💡 Future Enhancements

- Add a booking system with calendar
- Integrate payment gateway for online purchases
- Add product catalog for fashion and perfumes
- Implement user authentication and profiles
- Add a blog section for beauty tips
- Create an email newsletter signup
- Add live chat support

---

## 📞 Support

For questions or issues, please contact the developer or refer to Django documentation:
- **Django Docs**: https://docs.djangoproject.com/
- **Tailwind Docs**: https://tailwindcss.com/docs

---

## 📄 License

This is a custom project template created for **Her Beauty Hub**. Feel free to modify and use as needed.

---

**Designed with 💕 for Her Beauty Hub**

*Empowering women through beauty, style, and confidence.*

