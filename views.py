"""
Views for Her Beauty Hub
Place this file in your Django app directory
"""

from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    """Home page view"""
    context = {
        'page_title': 'Home',
    }
    return render(request, 'index.html', context)


def about(request):
    """About page view"""
    context = {
        'page_title': 'About Us',
    }
    return render(request, 'about.html', context)


def services(request):
    """Services page view"""
    context = {
        'page_title': 'Our Services',
        'services': [
            {
                'name': 'Hair Styling',
                'description': 'Expert hair styling for every occasion',
                'icon': 'fa-cut'
            },
            {
                'name': 'Hair Treatment',
                'description': 'Revitalize and restore your hair',
                'icon': 'fa-spa'
            },
            {
                'name': 'Clothing & Fashion',
                'description': 'Trendy outfits and elegant dresses',
                'icon': 'fa-tshirt'
            },
            {
                'name': 'Perfume Sales',
                'description': 'Premium fragrances collection',
                'icon': 'fa-spray-can'
            },
            {
                'name': 'Make-up & Beauty Care',
                'description': 'Professional makeup services',
                'icon': 'fa-palette'
            },
            {
                'name': 'Beauty Consultation',
                'description': 'Expert guidance for your perfect look',
                'icon': 'fa-comments'
            },
        ]
    }
    return render(request, 'services.html', context)


def gallery(request):
    """Gallery page view"""
    context = {
        'page_title': 'Gallery',
    }
    return render(request, 'gallery.html', context)


def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        message = request.POST.get('message')
        
        # Validate required fields
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')
        
        # TODO: Add your form processing logic here
        # Examples:
        # - Save to database
        # - Send email notification
        # - Integrate with CRM
        
        # For now, just show success message
        messages.success(
            request, 
            f'Thank you {name}! We received your message and will get back to you soon.'
        )
        
        # Redirect to avoid form resubmission
        return redirect('contact')
    
    context = {
        'page_title': 'Contact Us',
    }
    return render(request, 'contact.html', context)

