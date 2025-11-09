"""
Views for Her Beauty Hub - Enhanced Professional Version
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import (
    Service, Product, GalleryItem, Testimonial,
    Video, DailyOffer, Currency, BusinessInfo,
    HairStyle, Perfume, ClothingItem, OrderMessage
)
from .forms import ContactMessageForm, BookingForm, OrderMessageForm


def index(request):
    """
    Enhanced home page view with videos, offers, and more
    """
    # Get featured services (max 3 for home page)
    featured_services = Service.objects.filter(active=True, featured=True)[:3]
    
    # Get featured products (max 6 for home page)
    featured_products = Product.objects.filter(available=True, featured=True)[:6]
    
    # Get approved and featured testimonials for home page
    testimonials = Testimonial.objects.filter(approved=True, featured=True)[:3]
    
    # Get recent gallery items for preview
    gallery_preview = GalleryItem.objects.all()[:6]
    
    # Get featured videos
    featured_videos = Video.objects.filter(active=True, featured=True)[:3]
    
    # Get active daily offers
    from datetime import date
    today = date.today()
    active_offers = DailyOffer.objects.filter(
        active=True,
        featured=True,
        start_date__lte=today,
        end_date__gte=today
    )[:3]
    
    # Get business info
    business_info = BusinessInfo.get_instance()
    
    context = {
        'featured_services': featured_services,
        'featured_products': featured_products,
        'testimonials': testimonials,
        'gallery_preview': gallery_preview,
        'featured_videos': featured_videos,
        'active_offers': active_offers,
        'business_info': business_info,
    }
    
    return render(request, 'index.html', context)


def about(request):
    """
    About page view - mostly static content
    """
    # Could add team members or dynamic content here in the future
    context = {}
    return render(request, 'about.html', context)


def services(request):
    """
    Services page view - displays all active services
    """
    # Get all active services
    all_services = Service.objects.filter(active=True)
    
    # Get testimonials related to services
    service_testimonials = Testimonial.objects.filter(
        approved=True,
        service__isnull=False
    )[:6]
    
    context = {
        'services': all_services,
        'testimonials': service_testimonials,
    }
    
    return render(request, 'services.html', context)


def gallery(request):
    """
    Gallery page view - displays all gallery items
    """
    # Get all gallery items
    gallery_items = GalleryItem.objects.all()
    
    # Optional: filter by category if provided
    category = request.GET.get('category')
    if category:
        gallery_items = gallery_items.filter(category__icontains=category)
    
    # Get unique categories for filter
    categories = GalleryItem.objects.values_list('category', flat=True).distinct()
    categories = [cat for cat in categories if cat]  # Remove empty strings
    
    context = {
        'gallery_items': gallery_items,
        'categories': categories,
        'selected_category': category,
    }
    
    return render(request, 'gallery.html', context)


def contact(request):
    """
    Contact page view with form submission
    """
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact_message = form.save()
            
            # Send success message to user
            messages.success(
                request,
                f'Thank you {contact_message.name}! We received your message and will get back to you soon.'
            )
            
            # Optional: Send email notification to admin
            try:
                send_mail(
                    subject=f'New Contact Message from {contact_message.name}',
                    message=f'Name: {contact_message.name}\nEmail: {contact_message.email}\n\nMessage:\n{contact_message.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@herbeautyhub.com',
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't break the flow
                print(f"Email sending failed: {e}")
            
            # Redirect to prevent form resubmission
            return redirect('contact')
    else:
        form = ContactMessageForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'contact.html', context)


def booking(request):
    """
    Booking page view for appointment scheduling with instant notifications
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the booking
            booking = form.save()
            
            # Send success message to user
            messages.success(
                request,
                f'Thank you {booking.name}! Your booking request for {booking.service.name} on {booking.date} has been received. We will confirm your appointment soon.'
            )
            
            # INSTANT NOTIFICATIONS TO OWNER
            from .notifications import send_booking_notification, send_telegram_notification
            
            # Send notifications via all available channels
            notifications_sent = send_booking_notification(booking)
            
            # Also try Telegram (if configured)
            telegram_msg = f"🎉 <b>NEW BOOKING!</b>\n\n👤 {booking.name}\n💇 {booking.service.name}\n📅 {booking.date}\n💰 Check admin panel!"
            send_telegram_notification(telegram_msg)
            
            # Log for debugging
            print(f"📬 Notifications sent via: {', '.join(notifications_sent) if notifications_sent else 'Console only'}")
            
            # Redirect to prevent form resubmission
            return redirect('booking')
    else:
        form = BookingForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'booking.html', context)


def products(request):
    """
    Enhanced products page view with pricing and reviews
    """
    # Get all available products
    all_products = Product.objects.filter(available=True)
    
    # Optional: filter by category
    category = request.GET.get('category')
    if category:
        all_products = all_products.filter(category=category)
    
    # Get active currencies
    currencies = Currency.objects.filter(active=True)
    
    # Get unique categories
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': all_products,
        'categories': categories,
        'selected_category': category,
        'currencies': currencies,
    }
    
    return render(request, 'products.html', context)


def videos(request):
    """
    Video gallery page view
    """
    # Get all active videos
    all_videos = Video.objects.filter(active=True)
    
    # Optional: filter by category
    category = request.GET.get('category')
    if category:
        all_videos = all_videos.filter(category=category)
    
    # Get featured videos
    featured_videos = all_videos.filter(featured=True)[:3]
    
    # Get unique categories
    categories = Video.CATEGORY_CHOICES
    
    context = {
        'videos': all_videos,
        'featured_videos': featured_videos,
        'categories': categories,
        'selected_category': category,
    }
    
    return render(request, 'videos.html', context)


def video_detail(request, video_id):
    """
    Individual video view page
    """
    video = get_object_or_404(Video, id=video_id, active=True)
    
    # Increment view count
    video.increment_views()
    
    # Get related videos (same category)
    related_videos = Video.objects.filter(
        category=video.category,
        active=True
    ).exclude(id=video.id)[:4]
    
    context = {
        'video': video,
        'related_videos': related_videos,
    }
    
    return render(request, 'video_detail.html', context)


def offers(request):
    """
    Daily offers and deals page
    """
    from datetime import date
    
    # Get all valid offers
    today = date.today()
    all_offers = DailyOffer.objects.filter(
        active=True,
        start_date__lte=today,
        end_date__gte=today
    )
    
    # Get featured offers
    featured_offers = all_offers.filter(featured=True)
    
    context = {
        'offers': all_offers,
        'featured_offers': featured_offers,
    }
    
    return render(request, 'offers.html', context)


def offer_detail(request, offer_id):
    """
    Individual offer detail page
    """
    offer = get_object_or_404(DailyOffer, id=offer_id)
    
    context = {
        'offer': offer,
    }
    
    return render(request, 'offer_detail.html', context)


def hairstyles(request):
    """Hair styles listing page"""
    hairstyles = HairStyle.objects.filter(available=True)
    return render(request, 'hairstyles.html', {'hairstyles': hairstyles})


def hairstyle_detail(request, pk):
    """Hair style detail with order form and instant notifications"""
    hairstyle = get_object_or_404(HairStyle, pk=pk)
    form = OrderMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        msg = form.save(commit=False)
        msg.product_type = "Hairstyle"
        msg.product_name = hairstyle.name
        msg.product_price_ksh = hairstyle.price_ksh
        msg.save()
        
        # INSTANT NOTIFICATION TO OWNER
        from .notifications import send_order_notification, send_telegram_notification
        send_order_notification(msg)
        
        # Quick Telegram alert
        telegram_msg = f"🎉 <b>NEW HAIRSTYLE BOOKING!</b>\n\n👤 {msg.name}\n💇 {msg.product_name}\n💰 KSH {int(msg.total_amount_ksh)}\n📋 #{msg.order_number}"
        send_telegram_notification(telegram_msg)
        
        messages.success(request, f'Thank you! Your booking for {hairstyle.name} has been confirmed. Order #: {msg.order_number}')
        return redirect('order_receipt', order_id=msg.id)
    return render(request, 'hairstyle_detail.html', {'hairstyle': hairstyle, 'form': form})


def perfumes(request):
    """Perfumes listing page"""
    perfumes = Perfume.objects.filter(available=True)
    return render(request, 'perfumes.html', {'perfumes': perfumes})


def perfume_detail(request, pk):
    """Perfume detail with order form and instant notifications"""
    perfume = get_object_or_404(Perfume, pk=pk)
    form = OrderMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        msg = form.save(commit=False)
        msg.product_type = "Perfume"
        msg.product_name = perfume.name
        msg.product_price_ksh = perfume.price_ksh
        msg.save()
        
        # INSTANT NOTIFICATION TO OWNER
        from .notifications import send_order_notification, send_telegram_notification
        send_order_notification(msg)
        telegram_msg = f"🌸 <b>NEW PERFUME ORDER!</b>\n\n👤 {msg.name}\n🌸 {msg.product_name}\n💰 KSH {int(msg.total_amount_ksh)}\n📋 #{msg.order_number}"
        send_telegram_notification(telegram_msg)
        
        messages.success(request, f'Thank you! Your order for {perfume.name} has been confirmed. Order #: {msg.order_number}')
        return redirect('order_receipt', order_id=msg.id)
    return render(request, 'perfume_detail.html', {'perfume': perfume, 'form': form})


def clothes(request):
    """Clothing items listing page"""
    clothes = ClothingItem.objects.filter(available=True)
    return render(request, 'clothes.html', {'clothes': clothes})


def clothes_detail(request, pk):
    """Clothing item detail with order form and instant notifications"""
    item = get_object_or_404(ClothingItem, pk=pk)
    form = OrderMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        msg = form.save(commit=False)
        msg.product_type = "Clothing"
        msg.product_name = item.name
        msg.product_price_ksh = item.price_ksh
        msg.save()
        
        # INSTANT NOTIFICATION TO OWNER
        from .notifications import send_order_notification, send_telegram_notification
        send_order_notification(msg)
        telegram_msg = f"👗 <b>NEW FASHION ORDER!</b>\n\n👤 {msg.name}\n👗 {msg.product_name}\n💰 KSH {int(msg.total_amount_ksh)}\n📋 #{msg.order_number}"
        send_telegram_notification(telegram_msg)
        
        messages.success(request, f'Thank you! Your order for {item.name} has been confirmed. Order #: {msg.order_number}')
        return redirect('order_receipt', order_id=msg.id)
    return render(request, 'clothes_detail.html', {'item': item, 'form': form})


def order_receipt(request, order_id):
    """Display and download receipt for order"""
    order = get_object_or_404(OrderMessage, id=order_id)
    
    context = {
        'order': order,
    }
    
    return render(request, 'order_receipt.html', context)

