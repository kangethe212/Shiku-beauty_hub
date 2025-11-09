"""
Models for Her Beauty Hub - Enhanced Professional Version
"""
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.utils import timezone
from datetime import date, timedelta


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

