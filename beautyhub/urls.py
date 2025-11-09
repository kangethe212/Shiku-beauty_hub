"""
URL configuration for beautyhub app - Enhanced Professional Version
"""
from django.urls import path
from . import views

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
]

