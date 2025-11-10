"""
Models for Her Beauty Hub - Enhanced Professional Version
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.utils import timezone
from datetime import date, timedelta
import random
import string


class Service(models.Model):
    """
    Service model for hair, beauty, and fashion services
    """
    name = models.CharField(max_length=200, help_text="Service name (e.g., Hair Styling)")
    description = models.TextField(help_text="Detailed description of the service")
    image = models.ImageField(
        upload_to='services/', 
        blank=True, 
        null=True,
        help_text="Service image (optional)"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Starting price (optional, e.g., 30.00)"
    )
    duration = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Service duration (e.g., '1-2 hours')"
    )
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome icon class (e.g., 'fa-cut')"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Display on home page?"
    )
    active = models.BooleanField(
        default=True,
        help_text="Is this service currently available?"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

    def get_price_display(self):
        """Return formatted price"""
        if self.price:
            return f"${self.price}"
        return "Contact for pricing"


class Product(models.Model):
    """
    Enhanced Product model with international pricing support
    """
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion & Clothing'),
        ('perfume', 'Perfumes & Fragrances'),
        ('beauty', 'Beauty Products'),
        ('accessories', 'Accessories'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fashion')
    image = models.ImageField(upload_to='products/', help_text="Product image")
    
    # Pricing (Base Currency)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price in base currency"
    )
    
    # International pricing
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price in USD (optional)"
    )
    price_eur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price in EUR (optional)"
    )
    price_gbp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price in GBP (optional)"
    )
    
    # Stock and availability
    stock_quantity = models.IntegerField(default=0, help_text="Quantity in stock")
    low_stock_threshold = models.IntegerField(default=5, help_text="Low stock alert threshold")
    available = models.BooleanField(default=True, help_text="In stock?")
    featured = models.BooleanField(default=False, help_text="Display on home page?")
    
    # Additional product info
    sku = models.CharField(max_length=100, blank=True, help_text="Stock Keeping Unit")
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Product weight (kg)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def get_category_display_name(self):
        """Return friendly category name"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def is_low_stock(self):
        """Check if product is low on stock"""
        return self.stock_quantity <= self.low_stock_threshold and self.stock_quantity > 0
    
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.stock_quantity == 0
    
    def get_price_in_currency(self, currency_code):
        """Get price in specified currency"""
        currency_map = {
            'USD': self.price_usd,
            'EUR': self.price_eur,
            'GBP': self.price_gbp,
        }
        return currency_map.get(currency_code.upper(), self.price)
    
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(approved=True)
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0
    
    def review_count(self):
        """Get number of approved reviews"""
        return self.reviews.filter(approved=True).count()


class GalleryItem(models.Model):
    """
    Gallery model for showcasing work
    """
    title = models.CharField(max_length=200, help_text="Image title or caption")
    description = models.TextField(
        blank=True,
        help_text="Optional description or details"
    )
    image = models.ImageField(upload_to='gallery/', help_text="Gallery image")
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category (e.g., 'Hair', 'Makeup', 'Fashion')"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Display prominently?"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return self.title
    
    def like_count(self):
        """Return total number of likes"""
        return self.likes.count()
    
    def comment_count(self):
        """Return total number of approved comments"""
        return self.comments.filter(approved=True).count()


class GalleryLike(models.Model):
    """
    Track likes on gallery items
    """
    gallery_item = models.ForeignKey(
        GalleryItem,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='gallery_likes',
        null=True,
        blank=True,
        help_text="User who liked (if logged in)"
    )
    # For guests (not logged in)
    session_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Session ID for guest likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Gallery Like"
        verbose_name_plural = "Gallery Likes"
        unique_together = [['gallery_item', 'user'], ['gallery_item', 'session_id']]
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} likes {self.gallery_item.title}"
        return f"Guest likes {self.gallery_item.title}"


class GalleryComment(models.Model):
    """
    Comments on gallery items
    """
    gallery_item = models.ForeignKey(
        GalleryItem,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='gallery_comments',
        null=True,
        blank=True,
        help_text="User who commented (if logged in)"
    )
    # For guests (not logged in)
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name for guest comments"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email for guest comments"
    )
    comment = models.TextField(help_text="Comment text")
    approved = models.BooleanField(
        default=True,
        help_text="Approve before showing publicly"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Gallery Comment"
        verbose_name_plural = "Gallery Comments"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f"Comment by {self.user.username} on {self.gallery_item.title}"
        return f"Comment by {self.name or 'Guest'} on {self.gallery_item.title}"
    
    def get_author_name(self):
        """Get comment author name"""
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.name or "Anonymous"


class Booking(models.Model):
    """
    Booking model for appointment requests
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200, help_text="Client's full name")
    email = models.EmailField(help_text="Client's email address")
    phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Contact phone number"
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings',
        help_text="Service to book"
    )
    date = models.DateField(help_text="Preferred appointment date")
    time = models.TimeField(
        blank=True,
        null=True,
        help_text="Preferred appointment time"
    )
    message = models.TextField(
        blank=True,
        help_text="Additional notes or requests"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date}"

    def is_upcoming(self):
        """Check if booking is in the future"""
        return self.date >= timezone.now().date()


class ContactMessage(models.Model):
    """
    Contact form submissions
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(
        max_length=200,
        blank=True,
        help_text="Message subject"
    )
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Testimonial(models.Model):
    """
    Customer testimonials and reviews
    """
    client_name = models.CharField(max_length=200)
    client_initial = models.CharField(
        max_length=1,
        blank=True,
        help_text="First letter of name (for avatar)"
    )
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1)],
        help_text="Rating out of 5"
    )
    testimonial = models.TextField(help_text="Customer review")
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials'
    )
    approved = models.BooleanField(
        default=False,
        help_text="Show on website?"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Display on home page?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.client_name} - {self.rating}⭐"

    def save(self, *args, **kwargs):
        """Auto-generate initial if not provided"""
        if not self.client_initial and self.client_name:
            self.client_initial = self.client_name[0].upper()
        super().save(*args, **kwargs)


class Video(models.Model):
    """
    Video model for promotional and tutorial videos
    """
    CATEGORY_CHOICES = [
        ('tutorial', 'Tutorial'),
        ('transformation', 'Transformation'),
        ('promotion', 'Promotion'),
        ('testimonial', 'Video Testimonial'),
        ('behind_scenes', 'Behind the Scenes'),
    ]

    title = models.CharField(max_length=200, help_text="Video title")
    description = models.TextField(help_text="Video description")
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'webm'])],
        help_text="Upload video file (MP4, MOV, AVI, WEBM)"
    )
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        help_text="Video thumbnail/preview image"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='promotion'
    )
    duration = models.CharField(
        max_length=20,
        blank=True,
        help_text="Video duration (e.g., '2:30')"
    )
    views = models.IntegerField(default=0, help_text="Number of views")
    featured = models.BooleanField(default=False, help_text="Feature on home page?")
    active = models.BooleanField(default=True, help_text="Is video active?")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title

    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])


class DailyOffer(models.Model):
    """
    Daily offers and special deals
    """
    title = models.CharField(max_length=200, help_text="Offer title")
    description = models.TextField(help_text="Offer details")
    image = models.ImageField(upload_to='offers/', help_text="Offer image")
    discount_percentage = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Discount percentage (e.g., 20 for 20% off)"
    )
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Original price"
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Discounted price (auto-calculated)"
    )
    start_date = models.DateField(help_text="Offer start date")
    end_date = models.DateField(help_text="Offer end date")
    terms_conditions = models.TextField(
        blank=True,
        help_text="Terms and conditions"
    )
    active = models.BooleanField(default=True, help_text="Is offer active?")
    featured = models.BooleanField(default=False, help_text="Feature prominently?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Daily Offer"
        verbose_name_plural = "Daily Offers"

    def __str__(self):
        return f"{self.title} - {self.discount_percentage}% OFF"

    def save(self, *args, **kwargs):
        """Auto-calculate discounted price"""
        if self.original_price and self.discount_percentage:
            discount_amount = (self.original_price * self.discount_percentage) / 100
            self.discounted_price = self.original_price - discount_amount
        super().save(*args, **kwargs)

    def is_valid(self):
        """Check if offer is currently valid"""
        today = date.today()
        return self.active and self.start_date <= today <= self.end_date

    def days_remaining(self):
        """Calculate days remaining"""
        if self.is_valid():
            return (self.end_date - date.today()).days
        return 0

    def savings_amount(self):
        """Calculate savings"""
        if self.original_price and self.discounted_price:
            return self.original_price - self.discounted_price
        return 0


class Currency(models.Model):
    """
    Currency model for international pricing
    """
    code = models.CharField(max_length=3, unique=True, help_text="Currency code (e.g., USD, EUR, NGN)")
    name = models.CharField(max_length=100, help_text="Currency name")
    symbol = models.CharField(max_length=10, help_text="Currency symbol (e.g., $, €, ₦)")
    exchange_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=1.0000,
        help_text="Exchange rate relative to base currency"
    )
    is_base = models.BooleanField(default=False, help_text="Is this the base currency?")
    active = models.BooleanField(default=True, help_text="Is currency active?")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.symbol})"


class ProductReview(models.Model):
    """
    Product reviews and ratings
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Rating 1-5"
    )
    review = models.TextField(help_text="Review text")
    approved = models.BooleanField(default=False, help_text="Approved for display?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"{self.product.name} - {self.rating}⭐ by {self.customer_name}"


class SocialMediaLink(models.Model):
    """
    Social media links management
    """
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('whatsapp', 'WhatsApp'),
        ('pinterest', 'Pinterest'),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(help_text="Full URL to your profile")
    username = models.CharField(max_length=100, help_text="Your username (optional)", blank=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"

    def __str__(self):
        return f"{self.get_platform_display()} - {self.username or self.url}"


class BusinessInfo(models.Model):
    """
    Business information (singleton pattern)
    """
    business_name = models.CharField(max_length=200, default="Her Beauty Hub")
    tagline = models.CharField(max_length=200, default="Glow. Style. Confidence.")
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=20, help_text="WhatsApp number with country code")
    
    # Business Hours
    weekday_hours = models.CharField(max_length=100, default="9:00 AM - 7:00 PM")
    saturday_hours = models.CharField(max_length=100, default="10:00 AM - 8:00 PM")
    sunday_hours = models.CharField(max_length=100, default="12:00 PM - 6:00 PM")
    
    # About
    about_text = models.TextField(help_text="About the business")
    mission = models.TextField(help_text="Mission statement")
    vision = models.TextField(help_text="Vision statement")
    
    # Logo and Images
    logo = models.ImageField(upload_to='business/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='business/', blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Information"
        verbose_name_plural = "Business Information"

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        """Ensure only one instance exists"""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class HairStyle(models.Model):
    """
    HairStyle model for different hair styling options
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='hairstyles/', blank=True, null=True)
    
    # Pricing in different currencies
    price_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Price in Kenyan Shillings (KSH)"
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price in USD (optional)"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Default price"
    )
    
    # Time duration
    duration_minutes = models.IntegerField(
        default=60,
        help_text="Duration in minutes (e.g., 120 for 2 hours)",
        validators=[MinValueValidator(1)]
    )
    duration = models.CharField(max_length=100, help_text="Display text (e.g., '2-3 hours')")
    
    difficulty = models.CharField(
        max_length=50,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('complex', 'Complex'),
        ],
        default='medium'
    )
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Hair Style"
        verbose_name_plural = "Hair Styles"

    def __str__(self):
        return f"{self.name} - KSH {self.price_ksh}"
    
    def duration_display(self):
        """Return formatted duration"""
        hours = self.duration_minutes // 60
        mins = self.duration_minutes % 60
        if hours > 0 and mins > 0:
            return f"{hours}h {mins}min"
        elif hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{mins} minutes"


class Perfume(models.Model):
    """
    Perfume model for fragrance products
    """
    SCENT_TYPES = [
        ('floral', 'Floral'),
        ('fruity', 'Fruity'),
        ('oriental', 'Oriental'),
        ('woody', 'Woody'),
        ('fresh', 'Fresh'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='perfumes/', blank=True, null=True)
    scent_type = models.CharField(max_length=50, choices=SCENT_TYPES)
    
    # Pricing
    price_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Price in Kenyan Shillings (KSH)"
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price in USD"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    volume = models.CharField(max_length=50, help_text="e.g., 50ml, 100ml")
    stock_quantity = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Perfume"
        verbose_name_plural = "Perfumes"

    def __str__(self):
        return f"{self.name} by {self.brand} - KSH {self.price_ksh}"


class ClothingItem(models.Model):
    """
    ClothingItem model for fashion products
    """
    SIZES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double XL'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='clothing/', blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('dress', 'Dress'),
            ('top', 'Top'),
            ('bottom', 'Bottom'),
            ('outfit', 'Complete Outfit'),
            ('accessory', 'Accessory'),
        ]
    )
    available_sizes = models.CharField(max_length=200, help_text="Available sizes (e.g., S, M, L)")
    
    # Pricing
    price_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Price in Kenyan Shillings (KSH)"
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price in USD"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    stock_quantity = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Clothing Item"
        verbose_name_plural = "Clothing Items"

    def __str__(self):
        return f"{self.name} - KSH {self.price_ksh}"


class OrderMessage(models.Model):
    """
    Order inquiry messages from customers with receipt generation
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    product_type = models.CharField(max_length=50, help_text="Hairstyle, Perfume, Clothing")
    product_name = models.CharField(max_length=200)
    product_price_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price in KSH"
    )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    total_amount_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Total in KSH"
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order Message"
        verbose_name_plural = "Order Messages"

    def __str__(self):
        return f"#{self.order_number} - {self.name} - {self.product_type}: {self.product_name}"
    
    def save(self, *args, **kwargs):
        """Generate order number and calculate total"""
        if not self.order_number:
            import random
            import string
            self.order_number = 'HBH' + ''.join(random.choices(string.digits, k=8))
        
        if self.product_price_ksh and self.quantity:
            self.total_amount_ksh = self.product_price_ksh * self.quantity
        
        super().save(*args, **kwargs)


# ============================================================
# MULTIPLE IMAGE MODELS (for galleries/sliders)
# ============================================================

class HairStyleImage(models.Model):
    """
    Multiple images for a single hairstyle (for image galleries)
    """
    hairstyle = models.ForeignKey(
        HairStyle,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='hairstyles/gallery/',
        help_text="Additional hairstyle photo"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional image caption"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = "Hairstyle Image"
        verbose_name_plural = "Hairstyle Images"
    
    def __str__(self):
        return f"Image for {self.hairstyle.name}"


class PerfumeImage(models.Model):
    """
    Multiple images for a single perfume (for image galleries)
    """
    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='perfumes/gallery/',
        help_text="Additional perfume photo"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional image caption"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = "Perfume Image"
        verbose_name_plural = "Perfume Images"
    
    def __str__(self):
        return f"Image for {self.perfume.name}"


class ClothingImage(models.Model):
    """
    Multiple images for a single clothing item (for image galleries)
    """
    clothing = models.ForeignKey(
        ClothingItem,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='clothing/gallery/',
        help_text="Additional clothing photo"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional image caption (e.g., 'Back view', 'Detail shot')"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = "Clothing Image"
        verbose_name_plural = "Clothing Images"
    
    def __str__(self):
        return f"Image for {self.clothing.name}"


# ============================================================
# LOYALTY & CUSTOMER ACCOUNT SYSTEM
# ============================================================

class UserProfile(models.Model):
    """
    Extended user profile with loyalty program features
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Personal Information
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        help_text="Birthday for special month discounts!"
    )
    
    # Student Verification
    is_student = models.BooleanField(
        default=False,
        help_text="Verified student status"
    )
    student_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Student ID number for verification"
    )
    university = models.CharField(
        max_length=200,
        blank=True,
        help_text="University/College name"
    )
    student_verified_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When student status was verified"
    )
    
    # Loyalty Points System
    loyalty_points = models.IntegerField(
        default=0,
        help_text="Earn 10 points per KSH 100 spent!"
    )
    total_points_earned = models.IntegerField(
        default=0,
        help_text="Lifetime points earned"
    )
    total_spent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Total amount spent (KSH)"
    )
    
    # Referral System
    referral_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        help_text="Unique referral code (auto-generated)"
    )
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals',
        help_text="Who referred this user"
    )
    referral_count = models.IntegerField(
        default=0,
        help_text="Number of friends referred"
    )
    
    # Account Status
    vip_status = models.BooleanField(
        default=False,
        help_text="VIP customer (5+ orders or 1000+ points)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.loyalty_points} pts"
    
    def save(self, *args, **kwargs):
        """Auto-generate referral code if not exists"""
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        
        # Check VIP status
        if self.loyalty_points >= 1000 or self.total_spent >= 5000:
            self.vip_status = True
        
        super().save(*args, **kwargs)
    
    def generate_referral_code(self):
        """Generate unique 6-character referral code"""
        while True:
            code = 'SBH' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not UserProfile.objects.filter(referral_code=code).exists():
                return code
    
    def is_birthday_month(self):
        """Check if current month is user's birthday month"""
        if not self.birthday:
            return False
        today = date.today()
        return today.month == self.birthday.month
    
    def get_discount_percentage(self):
        """Calculate available discount percentage"""
        discount = 0
        
        # Student discount: 10%
        if self.is_student:
            discount += 10
        
        # Birthday month: Extra 5%
        if self.is_birthday_month():
            discount += 5
        
        # VIP discount: Extra 5%
        if self.vip_status:
            discount += 5
        
        return min(discount, 25)  # Max 25% total discount
    
    def add_loyalty_points(self, amount_spent):
        """Add loyalty points based on amount spent (10 points per KSH 100)"""
        points_earned = int(amount_spent / 100) * 10
        self.loyalty_points += points_earned
        self.total_points_earned += points_earned
        self.total_spent += amount_spent
        self.save()
        return points_earned
    
    def redeem_points(self, points):
        """Redeem loyalty points (100 points = KSH 100 discount)"""
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            self.save()
            return True
        return False
    
    def points_to_currency(self):
        """Convert loyalty points to KSH value (100 points = KSH 100)"""
        return self.loyalty_points


class Wishlist(models.Model):
    """
    User's saved favorite products
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    
    # Product references (nullable to support all product types)
    hairstyle = models.ForeignKey(
        HairStyle,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    clothing = models.ForeignKey(
        ClothingItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        unique_together = [
            ['user', 'hairstyle'],
            ['user', 'perfume'],
            ['user', 'clothing']
        ]
    
    def __str__(self):
        product_name = "Unknown"
        if self.hairstyle:
            product_name = self.hairstyle.name
        elif self.perfume:
            product_name = self.perfume.name
        elif self.clothing:
            product_name = self.clothing.name
        return f"{self.user.username} - {product_name}"
    
    def get_product(self):
        """Return the actual product object"""
        if self.hairstyle:
            return self.hairstyle
        elif self.perfume:
            return self.perfume
        elif self.clothing:
            return self.clothing
        return None
    
    def get_product_type(self):
        """Return product type as string"""
        if self.hairstyle:
            return "Hairstyle"
        elif self.perfume:
            return "Perfume"
        elif self.clothing:
            return "Clothing"
        return "Unknown"


class Referral(models.Model):
    """
    Track referrals and rewards
    """
    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='referrals_made',
        help_text="User who referred"
    )
    referred_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='referred_by_relation',
        help_text="User who was referred"
    )
    referral_code_used = models.CharField(
        max_length=10,
        help_text="Referral code that was used"
    )
    
    # Rewards tracking
    reward_claimed = models.BooleanField(
        default=False,
        help_text="Has referrer claimed reward?"
    )
    reward_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of reward (e.g., '100 points', 'Free service')"
    )
    
    # Milestones
    referred_user_made_purchase = models.BooleanField(
        default=False,
        help_text="Has referred user made their first purchase?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referred_user.username}"
    
    def check_milestone_reward(self):
        """Check if referrer should get milestone rewards"""
        referrer_profile = self.referrer.profile
        total_referrals = referrer_profile.referral_count
        
        # Milestone rewards
        if total_referrals == 3:
            # 3 referrals = Free service
            self.reward_type = "Free service (up to KSH 800)"
            self.save()
        elif total_referrals == 5:
            # 5 referrals = 500 bonus points
            referrer_profile.loyalty_points += 500
            referrer_profile.save()
            self.reward_type = "500 bonus points"
            self.save()
        elif total_referrals == 10:
            # 10 referrals = VIP status
            referrer_profile.vip_status = True
            referrer_profile.save()
            self.reward_type = "VIP Status Unlocked!"
            self.save()


class Order(models.Model):
    """
    Enhanced order tracking for loyalty system
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True,
        help_text="Registered user (if applicable)"
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique order number"
    )
    
    # Customer info (for guest orders)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Product details
    product_type = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    
    # Pricing
    original_price_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Original price before discounts"
    )
    discount_percentage = models.IntegerField(
        default=0,
        help_text="Total discount applied (%)"
    )
    discount_amount_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Discount amount in KSH"
    )
    final_amount_ksh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Final amount paid"
    )
    
    # Loyalty points
    points_earned = models.IntegerField(
        default=0,
        help_text="Loyalty points earned from this order"
    )
    points_redeemed = models.IntegerField(
        default=0,
        help_text="Loyalty points used for discount"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        """Auto-generate order number and calculate final amount"""
        if not self.order_number:
            self.order_number = 'SBH' + ''.join(random.choices(string.digits, k=8))
        
        # Calculate discount amount
        self.discount_amount_ksh = (self.original_price_ksh * self.quantity) * (self.discount_percentage / 100)
        
        # Calculate final amount
        subtotal = self.original_price_ksh * self.quantity
        self.final_amount_ksh = subtotal - self.discount_amount_ksh
        
        # Deduct points redeemed (100 points = KSH 100)
        if self.points_redeemed > 0:
            points_value = self.points_redeemed  # 1:1 ratio
            self.final_amount_ksh = max(0, self.final_amount_ksh - points_value)
        
        super().save(*args, **kwargs)
        
        # Award loyalty points when order is completed
        if self.status == 'completed' and self.user and self.points_earned == 0:
            points = self.user.profile.add_loyalty_points(float(self.final_amount_ksh))
            self.points_earned = points
            super().save(*args, **kwargs)  # Save again to update points_earned

