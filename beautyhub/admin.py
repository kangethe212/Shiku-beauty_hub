"""
Admin configuration for Shiku Beauty Hub - ULTIMATE CONTROL CENTER
Full Frontend Control for University Entrepreneur
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count, Avg
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Service, Product, GalleryItem, Booking, ContactMessage, Testimonial,
    Video, DailyOffer, Currency, ProductReview, SocialMediaLink, BusinessInfo,
    HairStyle, Perfume, ClothingItem, OrderMessage,
    HairStyleImage, PerfumeImage, ClothingImage
)

# Customize Admin Site Header
admin.site.site_header = "Shiku Beauty Hub Control Center 💎"
admin.site.site_title = "Shiku Admin"
admin.site.index_title = "Welcome to Your Business Dashboard ✨"


# ============================================================
# INLINE ADMINS FOR MULTIPLE IMAGES
# ============================================================

class HairStyleImageInline(admin.TabularInline):
    """Inline admin for uploading multiple hairstyle images"""
    model = HairStyleImage
    extra = 3  # Show 3 empty upload fields by default
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"


class PerfumeImageInline(admin.TabularInline):
    """Inline admin for uploading multiple perfume images"""
    model = PerfumeImage
    extra = 3
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"


class ClothingImageInline(admin.TabularInline):
    """Inline admin for uploading multiple clothing images"""
    model = ClothingImage
    extra = 3
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Admin interface for Services
    """
    list_display = ['name', 'price', 'duration', 'featured', 'active', 'order', 'created_at']
    list_filter = ['active', 'featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['featured', 'active', 'order']
    ordering = ['order', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon_class')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration')
        }),
        ('Display Settings', {
            'fields': ('image', 'featured', 'active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Add booking count to queryset"""
        qs = super().get_queryset(request)
        return qs


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Products - Enhanced with international pricing
    """
    list_display = ['name', 'category', 'price', 'stock_status', 'stock_quantity', 'available', 'featured', 'average_rating', 'created_at']
    list_filter = ['category', 'available', 'featured', 'created_at']
    search_fields = ['name', 'description', 'sku']
    list_editable = ['available', 'featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'image_preview', 'stock_status_display', 'rating_display']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category', 'sku')
        }),
        ('Base Pricing', {
            'fields': ('price',)
        }),
        ('International Pricing (Optional)', {
            'fields': ('price_usd', 'price_eur', 'price_gbp'),
            'classes': ('collapse',)
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'low_stock_threshold', 'available', 'stock_status_display')
        }),
        ('Product Details', {
            'fields': ('weight',),
            'classes': ('collapse',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Display Settings', {
            'fields': ('featured', 'rating_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"
    
    def stock_status(self, obj):
        """Display stock status with color"""
        if obj.is_out_of_stock():
            return format_html('<span style="color: red; font-weight: bold;">OUT OF STOCK</span>')
        elif obj.is_low_stock():
            return format_html('<span style="color: orange; font-weight: bold;">LOW STOCK</span>')
        else:
            return format_html('<span style="color: green; font-weight: bold;">IN STOCK</span>')
    stock_status.short_description = "Status"
    
    def stock_status_display(self, obj):
        """Display stock status in detail view"""
        return self.stock_status(obj)
    stock_status_display.short_description = "Stock Status"
    
    def rating_display(self, obj):
        """Display product rating"""
        avg_rating = obj.average_rating()
        review_count = obj.review_count()
        if avg_rating > 0:
            stars = '⭐' * int(avg_rating)
            return format_html(
                '<span>{} ({} - {} reviews)</span>',
                stars, avg_rating, review_count
            )
        return "No reviews yet"
    rating_display.short_description = "Rating"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Gallery Items
    """
    list_display = ['title', 'category', 'featured', 'image_thumbnail', 'uploaded_at']
    list_filter = ['category', 'featured', 'uploaded_at']
    search_fields = ['title', 'description', 'category']
    list_editable = ['featured']
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at', 'image_preview']
    
    fieldsets = (
        ('Gallery Item', {
            'fields': ('title', 'description', 'category')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Settings', {
            'fields': ('featured', 'uploaded_at')
        }),
    )

    def image_thumbnail(self, obj):
        """Display small thumbnail in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = "Image"

    def image_preview(self, obj):
        """Display larger preview in detail view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for Bookings
    """
    list_display = ['name', 'email', 'service', 'date', 'time', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at', 'service']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('service', 'date', 'time', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']

    def mark_as_confirmed(self, request, queryset):
        """Bulk action to confirm bookings"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"

    def mark_as_completed(self, request, queryset):
        """Bulk action to mark bookings as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} booking(s) marked as completed.")
    mark_as_completed.short_description = "Mark selected bookings as completed"

    def mark_as_cancelled(self, request, queryset):
        """Bulk action to cancel bookings"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"{updated} booking(s) marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Contact Messages
    """
    list_display = ['name', 'email', 'subject_preview', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message', 'subject']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )

    def subject_preview(self, obj):
        """Show subject or message preview"""
        if obj.subject:
            return obj.subject[:50]
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    subject_preview.short_description = "Subject/Message"

    actions = ['mark_as_read', 'mark_as_replied']

    def mark_as_read(self, request, queryset):
        """Bulk action to mark messages as read"""
        updated = queryset.update(status='read')
        self.message_user(request, f"{updated} message(s) marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_replied(self, request, queryset):
        """Bulk action to mark messages as replied"""
        updated = queryset.update(status='replied')
        self.message_user(request, f"{updated} message(s) marked as replied.")
    mark_as_replied.short_description = "Mark selected messages as replied"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin interface for Testimonials
    """
    list_display = ['client_name', 'rating', 'service', 'approved', 'featured', 'created_at']
    list_filter = ['approved', 'featured', 'rating', 'created_at', 'service']
    search_fields = ['client_name', 'testimonial']
    list_editable = ['approved', 'featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_initial')
        }),
        ('Review', {
            'fields': ('rating', 'testimonial', 'service')
        }),
        ('Display Settings', {
            'fields': ('approved', 'featured', 'created_at')
        }),
    )

    actions = ['approve_testimonials', 'feature_testimonials']

    def approve_testimonials(self, request, queryset):
        """Bulk action to approve testimonials"""
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} testimonial(s) approved.")
    approve_testimonials.short_description = "Approve selected testimonials"

    def feature_testimonials(self, request, queryset):
        """Bulk action to feature testimonials"""
        updated = queryset.update(featured=True, approved=True)
        self.message_user(request, f"{updated} testimonial(s) featured on home page.")
    feature_testimonials.short_description = "Feature selected testimonials on home page"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Admin interface for Videos
    """
    list_display = ['title', 'category', 'duration', 'views', 'featured', 'active', 'thumbnail_preview', 'uploaded_at']
    list_filter = ['category', 'featured', 'active', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['featured', 'active']
    ordering = ['-uploaded_at']
    readonly_fields = ['views', 'uploaded_at', 'video_preview', 'thumbnail_image']

    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'description', 'category', 'duration')
        }),
        ('Files', {
            'fields': ('video_file', 'video_preview', 'thumbnail', 'thumbnail_image')
        }),
        ('Settings', {
            'fields': ('featured', 'active', 'views', 'uploaded_at')
        }),
    )

    def thumbnail_preview(self, obj):
        """Display small thumbnail in list"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 5px;" />',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_preview.short_description = "Preview"

    def thumbnail_image(self, obj):
        """Display larger thumbnail in detail"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_image.short_description = "Thumbnail Preview"

    def video_preview(self, obj):
        """Display video player in admin"""
        if obj.video_file:
            return format_html(
                '<video width="400" controls><source src="{}" type="video/mp4">Your browser does not support video.</video>',
                obj.video_file.url
            )
        return "No video"
    video_preview.short_description = "Video Preview"


@admin.register(DailyOffer)
class DailyOfferAdmin(admin.ModelAdmin):
    """
    Admin interface for Daily Offers
    """
    list_display = ['title', 'discount_percentage', 'original_price', 'discounted_price', 'start_date', 'end_date', 'days_remaining', 'active', 'featured']
    list_filter = ['active', 'featured', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    list_editable = ['active', 'featured']
    ordering = ['-created_at']
    readonly_fields = ['discounted_price', 'created_at', 'image_preview', 'offer_status']
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Offer Details', {
            'fields': ('title', 'description', 'image', 'image_preview')
        }),
        ('Pricing', {
            'fields': ('discount_percentage', 'original_price', 'discounted_price')
        }),
        ('Validity Period', {
            'fields': ('start_date', 'end_date', 'offer_status')
        }),
        ('Terms & Settings', {
            'fields': ('terms_conditions', 'active', 'featured')
        }),
    )

    def image_preview(self, obj):
        """Display offer image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"

    def offer_status(self, obj):
        """Display offer validity status"""
        if obj.is_valid():
            days = obj.days_remaining()
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ ACTIVE ({} days remaining)</span>',
                days
            )
        return format_html('<span style="color: red;">✗ Expired</span>')
    offer_status.short_description = "Status"


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """
    Admin interface for Currencies
    """
    list_display = ['code', 'name', 'symbol', 'exchange_rate', 'is_base', 'active', 'updated_at']
    list_filter = ['active', 'is_base']
    search_fields = ['code', 'name']
    list_editable = ['exchange_rate', 'active']
    ordering = ['code']

    fieldsets = (
        ('Currency Information', {
            'fields': ('code', 'name', 'symbol')
        }),
        ('Exchange Rate', {
            'fields': ('exchange_rate', 'is_base')
        }),
        ('Settings', {
            'fields': ('active', 'updated_at')
        }),
    )
    readonly_fields = ['updated_at']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Product Reviews
    """
    list_display = ['product', 'customer_name', 'rating', 'approved', 'created_at']
    list_filter = ['approved', 'rating', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'review', 'product__name']
    list_editable = ['approved']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Product', {
            'fields': ('product',)
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email')
        }),
        ('Review', {
            'fields': ('rating', 'review')
        }),
        ('Settings', {
            'fields': ('approved', 'created_at')
        }),
    )

    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        """Bulk approve reviews"""
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} review(s) approved.")
    approve_reviews.short_description = "Approve selected reviews"


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    """
    Admin interface for Social Media Links
    """
    list_display = ['platform', 'username', 'url', 'active', 'order']
    list_filter = ['platform', 'active']
    search_fields = ['platform', 'username', 'url']
    list_editable = ['active', 'order']
    ordering = ['order', 'platform']

    fieldsets = (
        ('Platform Information', {
            'fields': ('platform', 'username', 'url')
        }),
        ('Settings', {
            'fields': ('active', 'order')
        }),
    )


@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    """
    Admin interface for Business Information (Singleton)
    """
    fieldsets = (
        ('Basic Information', {
            'fields': ('business_name', 'tagline', 'phone', 'email', 'address', 'whatsapp_number')
        }),
        ('Business Hours', {
            'fields': ('weekday_hours', 'saturday_hours', 'sunday_hours')
        }),
        ('About Us', {
            'fields': ('about_text', 'mission', 'vision')
        }),
        ('Branding', {
            'fields': ('logo', 'hero_image')
        }),
    )
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        """Only allow one instance"""
        return not BusinessInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion"""
        return False


@admin.register(HairStyle)
class HairStyleAdmin(admin.ModelAdmin):
    """💇 Hair Styles - Complete Control"""
    list_display = ['image_thumb', 'name', 'price_ksh_display', 'price_usd_display', 'duration_display', 'difficulty', 'available', 'featured', 'view_count']
    list_filter = ['available', 'featured', 'difficulty', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['available', 'featured']
    readonly_fields = ['created_at', 'image_preview', 'duration_display']
    ordering = ['-featured', '-created_at']
    list_per_page = 20
    inlines = [HairStyleImageInline]  # Add multiple image uploads
    
    fieldsets = (
        ('📸 Main Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Main product image shown on listing pages'
        }),
        ('✨ Hair Style Information', {
            'fields': ('name', 'description')
        }),
        ('⏱️ Duration & Difficulty', {
            'fields': ('duration_minutes', 'duration', 'duration_display', 'difficulty')
        }),
        ('💰 Pricing (Student-Friendly)', {
            'fields': ('price_ksh', 'price_usd', 'price'),
            'description': 'KSH is the main price displayed to customers'
        }),
        ('⚙️ Display Settings', {
            'fields': ('available', 'featured'),
            'description': 'Featured styles appear first on the website'
        }),
        ('📅 Created', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'make_available', 'make_unavailable', 'duplicate_style']
    
    def image_thumb(self, obj):
        """Display thumbnail in list"""
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 10px;" />', obj.image.url)
        return format_html('<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #FF6B9D, #FFB7C5); border-radius: 10px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 24px;">💇</span></div>')
    image_thumb.short_description = "📸"
    
    def price_ksh_display(self, obj):
        """Display KSH price with formatting"""
        return format_html('<strong style="color: #FF6B9D; font-size: 14px;">KSH {}</strong>', int(obj.price_ksh))
    price_ksh_display.short_description = "💰 KSH Price"
    price_ksh_display.admin_order_field = 'price_ksh'
    
    def price_usd_display(self, obj):
        """Display USD price"""
        if obj.price_usd:
            return format_html('<span style="color: #666;">${}</span>', int(obj.price_usd))
        return "-"
    price_usd_display.short_description = "USD"
    
    def view_count(self, obj):
        """Show if popular (for future analytics)"""
        return "⭐" if obj.featured else "—"
    view_count.short_description = "Status"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 400px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />', obj.image.url)
        return format_html('<div style="padding: 60px; background: linear-gradient(135deg, #FF6B9D, #FFB7C5); border-radius: 15px; text-align: center;"><span style="font-size: 80px;">💇</span><p style="color: white; margin-top: 10px;">No Image Yet</p></div>')
    image_preview.short_description = "Image Preview"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"✨ {updated} hairstyle(s) marked as FEATURED!")
    make_featured.short_description = "⭐ Mark as FEATURED (show first)"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"Removed {updated} hairstyle(s) from featured.")
    remove_featured.short_description = "Remove from featured"
    
    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"✅ {updated} hairstyle(s) now AVAILABLE!")
    make_available.short_description = "✅ Make available for booking"
    
    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"❌ {updated} hairstyle(s) now unavailable.")
    make_unavailable.short_description = "❌ Make unavailable"
    
    def duplicate_style(self, request, queryset):
        """Duplicate selected hairstyles"""
        count = 0
        for style in queryset:
            style.pk = None
            style.name = f"{style.name} (Copy)"
            style.save()
            count += 1
        self.message_user(request, f"📋 Duplicated {count} hairstyle(s)!")
    duplicate_style.short_description = "📋 Duplicate selected styles"


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    """🌸 Perfumes - Complete Control"""
    list_display = ['image_thumb', 'name', 'brand', 'scent_type', 'volume', 'price_ksh_display', 'stock_display', 'available', 'featured']
    list_filter = ['available', 'featured', 'scent_type', 'brand', 'created_at']
    search_fields = ['name', 'brand', 'description']
    list_editable = ['available', 'featured']
    readonly_fields = ['created_at', 'image_preview']
    ordering = ['-featured', '-created_at']
    list_per_page = 20
    inlines = [PerfumeImageInline]  # Add multiple image uploads
    
    fieldsets = (
        ('📸 Image', {
            'fields': ('image', 'image_preview')
        }),
        ('🌸 Perfume Information', {
            'fields': ('name', 'brand', 'description', 'scent_type', 'volume')
        }),
        ('💰 Pricing (Student-Friendly)', {
            'fields': ('price_ksh', 'price_usd', 'price'),
            'description': 'KSH is the main price displayed to customers'
        }),
        ('📦 Stock Management', {
            'fields': ('stock_quantity',),
            'description': 'Track inventory - students will see stock status'
        }),
        ('⚙️ Display Settings', {
            'fields': ('available', 'featured'),
            'description': 'Featured perfumes appear first with ⭐ BESTSELLER badge'
        }),
        ('📅 Created', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'make_available', 'make_unavailable', 'add_stock', 'low_stock_alert']
    
    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 10px;" />', obj.image.url)
        return format_html('<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #C77DFF, #E0AAFF); border-radius: 10px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 24px;">🌸</span></div>')
    image_thumb.short_description = "📸"
    
    def price_ksh_display(self, obj):
        return format_html('<strong style="color: #C77DFF; font-size: 14px;">KSH {}</strong>', int(obj.price_ksh))
    price_ksh_display.short_description = "💰 KSH Price"
    price_ksh_display.admin_order_field = 'price_ksh'
    
    def stock_display(self, obj):
        if obj.stock_quantity <= 5:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ {} left</span>', obj.stock_quantity)
        elif obj.stock_quantity <= 10:
            return format_html('<span style="color: orange; font-weight: bold;">{} left</span>', obj.stock_quantity)
        return format_html('<span style="color: green;">✓ {}</span>', obj.stock_quantity)
    stock_display.short_description = "📦 Stock"
    stock_display.admin_order_field = 'stock_quantity'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 400px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />', obj.image.url)
        return format_html('<div style="padding: 60px; background: linear-gradient(135deg, #C77DFF, #E0AAFF); border-radius: 15px; text-align: center;"><span style="font-size: 80px;">🌸</span><p style="color: white; margin-top: 10px;">No Image Yet</p></div>')
    image_preview.short_description = "Image Preview"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"⭐ {updated} perfume(s) marked as BESTSELLER!")
    make_featured.short_description = "⭐ Mark as BESTSELLER"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"Removed {updated} perfume(s) from bestsellers.")
    remove_featured.short_description = "Remove from bestsellers"
    
    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"✅ {updated} perfume(s) now AVAILABLE!")
    make_available.short_description = "✅ Make available"
    
    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"❌ {updated} perfume(s) now unavailable.")
    make_unavailable.short_description = "❌ Make unavailable"
    
    def add_stock(self, request, queryset):
        for perfume in queryset:
            perfume.stock_quantity += 10
            perfume.save()
        self.message_user(request, f"📦 Added 10 units to {queryset.count()} perfume(s)!")
    add_stock.short_description = "📦 Add 10 units to stock"
    
    def low_stock_alert(self, request, queryset):
        low_stock = queryset.filter(stock_quantity__lte=5)
        count = low_stock.count()
        if count > 0:
            self.message_user(request, f"⚠️ {count} perfume(s) have LOW STOCK (≤5 units)!", level='WARNING')
        else:
            self.message_user(request, "✅ All selected perfumes have good stock levels!")
    low_stock_alert.short_description = "⚠️ Check stock levels"


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    """👗 Fashion - Complete Control"""
    list_display = ['image_thumb', 'name', 'category', 'sizes_display', 'price_ksh_display', 'stock_display', 'available', 'featured']
    list_filter = ['available', 'featured', 'category', 'created_at']
    search_fields = ['name', 'description', 'available_sizes']
    list_editable = ['available', 'featured']
    readonly_fields = ['created_at', 'image_preview']
    ordering = ['-featured', '-created_at']
    list_per_page = 20
    inlines = [ClothingImageInline]  # Add multiple image uploads
    
    fieldsets = (
        ('📸 Image', {
            'fields': ('image', 'image_preview')
        }),
        ('👗 Clothing Information', {
            'fields': ('name', 'description', 'category', 'available_sizes')
        }),
        ('💰 Pricing (Student-Friendly)', {
            'fields': ('price_ksh', 'price_usd', 'price'),
            'description': 'KSH is the main price displayed to customers'
        }),
        ('📦 Stock Management', {
            'fields': ('stock_quantity',),
            'description': 'Track inventory - students will see stock status'
        }),
        ('⚙️ Display Settings', {
            'fields': ('available', 'featured'),
            'description': 'Featured items appear first with 🔥 TRENDING badge'
        }),
        ('📅 Created', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'make_available', 'make_unavailable', 'add_stock', 'duplicate_item']
    
    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 10px;" />', obj.image.url)
        return format_html('<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #FFD700, #FFE44D); border-radius: 10px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 24px;">👗</span></div>')
    image_thumb.short_description = "📸"
    
    def sizes_display(self, obj):
        return format_html('<span style="font-size: 11px; background: #f0f0f0; padding: 3px 8px; border-radius: 5px;">{}</span>', obj.available_sizes)
    sizes_display.short_description = "Sizes"
    
    def price_ksh_display(self, obj):
        return format_html('<strong style="color: #FFD700; font-size: 14px;">KSH {}</strong>', int(obj.price_ksh))
    price_ksh_display.short_description = "💰 KSH Price"
    price_ksh_display.admin_order_field = 'price_ksh'
    
    def stock_display(self, obj):
        if obj.stock_quantity <= 3:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ {} left</span>', obj.stock_quantity)
        elif obj.stock_quantity <= 10:
            return format_html('<span style="color: orange; font-weight: bold;">{} left</span>', obj.stock_quantity)
        return format_html('<span style="color: green;">✓ {}</span>', obj.stock_quantity)
    stock_display.short_description = "📦 Stock"
    stock_display.admin_order_field = 'stock_quantity'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 400px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />', obj.image.url)
        return format_html('<div style="padding: 60px; background: linear-gradient(135deg, #FFD700, #FFE44D); border-radius: 15px; text-align: center;"><span style="font-size: 80px;">👗</span><p style="color: white; margin-top: 10px;">No Image Yet</p></div>')
    image_preview.short_description = "Image Preview"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"🔥 {updated} item(s) marked as TRENDING!")
    make_featured.short_description = "🔥 Mark as TRENDING"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"Removed {updated} item(s) from trending.")
    remove_featured.short_description = "Remove from trending"
    
    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"✅ {updated} item(s) now AVAILABLE!")
    make_available.short_description = "✅ Make available"
    
    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"❌ {updated} item(s) now unavailable.")
    make_unavailable.short_description = "❌ Make unavailable"
    
    def add_stock(self, request, queryset):
        for item in queryset:
            item.stock_quantity += 5
            item.save()
        self.message_user(request, f"📦 Added 5 units to {queryset.count()} item(s)!")
    add_stock.short_description = "📦 Add 5 units to stock"
    
    def duplicate_item(self, request, queryset):
        count = 0
        for item in queryset:
            item.pk = None
            item.name = f"{item.name} (Copy)"
            item.save()
            count += 1
        self.message_user(request, f"📋 Duplicated {count} item(s)!")
    duplicate_item.short_description = "📋 Duplicate selected items"


@admin.register(OrderMessage)
class OrderMessageAdmin(admin.ModelAdmin):
    """🛒 Student Orders - Complete Control"""
    list_display = ['order_badge', 'customer_info', 'product_info', 'amount_display', 'status_display', 'date_display']
    list_filter = ['product_type', 'status', 'created_at']
    search_fields = ['order_number', 'name', 'email', 'product_name', 'phone']
    readonly_fields = ['order_number', 'total_amount_ksh', 'created_at']
    list_editable = []
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('📋 Order Information', {
            'fields': ('order_number', 'status', 'created_at')
        }),
        ('👤 Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('🛍️ Product Details', {
            'fields': ('product_type', 'product_name', 'product_price_ksh', 'quantity', 'total_amount_ksh')
        }),
        ('💬 Customer Message', {
            'fields': ('message',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_pending', 'mark_as_cancelled', 'export_orders']
    
    def order_badge(self, obj):
        """Display order number as badge"""
        colors = {
            'pending': '#FFA500',
            'confirmed': '#3B82F6',
            'completed': '#10B981',
            'cancelled': '#EF4444'
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.order_number
        )
    order_badge.short_description = "Order #"
    
    def customer_info(self, obj):
        """Display customer details"""
        phone = f'📱 {obj.phone}' if obj.phone else ''
        return format_html(
            '<div style="line-height: 1.4;"><strong>{}</strong><br/><small>✉️ {}</small><br/><small>{}</small></div>',
            obj.name, obj.email, phone
        )
    customer_info.short_description = "👤 Customer"
    
    def product_info(self, obj):
        """Display product details with type badge"""
        type_colors = {
            'Hairstyle': '#FF6B9D',
            'Perfume': '#C77DFF',
            'Clothing': '#FFD700'
        }
        type_icons = {
            'Hairstyle': '💇',
            'Perfume': '🌸',
            'Clothing': '👗'
        }
        color = type_colors.get(obj.product_type, '#6B7280')
        icon = type_icons.get(obj.product_type, '📦')
        return format_html(
            '<div><span style="background: {}; color: white; padding: 2px 8px; border-radius: 5px; font-size: 10px; font-weight: bold;">{} {}</span><br/><strong style="margin-top: 4px; display: inline-block;">{}</strong><br/><small>Qty: {}</small></div>',
            color, icon, obj.product_type, obj.product_name, obj.quantity
        )
    product_info.short_description = "🛍️ Product"
    
    def amount_display(self, obj):
        """Display total amount"""
        return format_html(
            '<div style="text-align: right;"><strong style="color: #10B981; font-size: 16px;">KSH {}</strong><br/><small style="color: #6B7280;">@ KSH {} each</small></div>',
            int(obj.total_amount_ksh), int(obj.product_price_ksh)
        )
    amount_display.short_description = "💰 Amount"
    amount_display.admin_order_field = 'total_amount_ksh'
    
    def status_display(self, obj):
        """Display status with icon"""
        status_config = {
            'pending': ('⏳', 'Pending', '#FFA500'),
            'confirmed': ('✅', 'Confirmed', '#3B82F6'),
            'completed': ('🎉', 'Completed', '#10B981'),
            'cancelled': ('❌', 'Cancelled', '#EF4444')
        }
        icon, text, color = status_config.get(obj.status, ('•', obj.status, '#6B7280'))
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 13px;">{} {}</span>',
            color, icon, text
        )
    status_display.short_description = "Status"
    status_display.admin_order_field = 'status'
    
    def date_display(self, obj):
        """Display date in friendly format"""
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days == 0:
            if diff.seconds < 3600:
                mins = diff.seconds // 60
                time_str = f"{mins} min ago"
            else:
                hours = diff.seconds // 3600
                time_str = f"{hours}h ago"
        elif diff.days == 1:
            time_str = "Yesterday"
        elif diff.days < 7:
            time_str = f"{diff.days} days ago"
        else:
            time_str = obj.created_at.strftime("%b %d, %Y")
        
        return format_html(
            '<div style="font-size: 12px;"><strong>{}</strong><br/><small style="color: #6B7280;">{}</small></div>',
            time_str, obj.created_at.strftime("%I:%M %p")
        )
    date_display.short_description = "📅 Date"
    date_display.admin_order_field = 'created_at'
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"✅ {updated} order(s) CONFIRMED! Students will be notified.")
    mark_as_confirmed.short_description = "✅ Confirm selected orders"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"🎉 {updated} order(s) marked as COMPLETED!")
    mark_as_completed.short_description = "🎉 Mark as completed"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f"⏳ {updated} order(s) set to pending.")
    mark_as_pending.short_description = "⏳ Set to pending"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"❌ {updated} order(s) cancelled.")
    mark_as_cancelled.short_description = "❌ Cancel selected orders"
    
    def export_orders(self, request, queryset):
        """Export selected orders summary"""
        total = queryset.aggregate(total=Sum('total_amount_ksh'))['total'] or 0
        count = queryset.count()
        self.message_user(request, f"📊 {count} orders selected | Total: KSH {int(total)}")
    export_orders.short_description = "📊 Calculate total sales"

