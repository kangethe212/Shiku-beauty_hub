"""
URL configuration for beautyhub app - Enhanced Professional Version
"""
from django.urls import path
from . import views
from . import views_loyalty

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    
    # Products
    path('products/', views.products, name='products'),
    
    # Videos
    path('videos/', views.videos, name='videos'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    
    # Offers
    path('offers/', views.offers, name='offers'),
    path('offer/<int:offer_id>/', views.offer_detail, name='offer_detail'),
    
    # Hair Styles
    path('hairstyles/', views.hairstyles, name='hairstyles'),
    path('hairstyle/<int:pk>/', views.hairstyle_detail, name='hairstyle_detail'),
    
    # Perfumes
    path('perfumes/', views.perfumes, name='perfumes'),
    path('perfume/<int:pk>/', views.perfume_detail, name='perfume_detail'),
    
    # Clothes
    path('clothes/', views.clothes, name='clothes'),
    path('clothes/<int:pk>/', views.clothes_detail, name='clothes_detail'),
    
    # Order Receipt
    path('receipt/<int:order_id>/', views.order_receipt, name='order_receipt'),
    
    # ============================================================
    # LOYALTY & CUSTOMER ACCOUNT SYSTEM
    # ============================================================
    
    # Authentication
    path('signup/', views_loyalty.signup_view, name='signup'),
    path('login/', views_loyalty.login_view, name='login'),
    path('logout/', views_loyalty.logout_view, name='logout'),
    
    # User Dashboard
    path('dashboard/', views_loyalty.dashboard_view, name='dashboard'),
    path('profile/settings/', views_loyalty.profile_settings_view, name='profile_settings'),
    
    # Wishlist
    path('wishlist/', views_loyalty.wishlist_view, name='wishlist'),
    path('wishlist/add/<str:product_type>/<int:product_id>/', views_loyalty.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views_loyalty.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/check/<str:product_type>/<int:product_id>/', views_loyalty.check_wishlist_status, name='check_wishlist_status'),
    
    # Orders & History
    path('orders/', views_loyalty.order_history_view, name='order_history'),
    
    # Referrals
    path('referrals/', views_loyalty.referrals_view, name='referrals'),
    
    # ============================================================
    # GALLERY ENGAGEMENT - LIKES & COMMENTS
    # ============================================================
    path('gallery/like/<int:gallery_id>/', views.gallery_like, name='gallery_like'),
    path('gallery/comment/<int:gallery_id>/', views.gallery_comment, name='gallery_comment'),
    path('gallery/check-like/<int:gallery_id>/', views.check_gallery_like_status, name='check_gallery_like'),
]

