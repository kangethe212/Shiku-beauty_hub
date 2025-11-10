"""
Views for Loyalty & Customer Account System
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import UserProfile, Wishlist, Referral, Order, HairStyle, Perfume, ClothingItem
from .forms import SignUpForm, LoginForm, UserProfileForm, UserUpdateForm


def signup_view(request):
    """
    User registration with loyalty program enrollment
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save()
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            # Update profile with additional info
            profile = user.profile
            profile.phone = form.cleaned_data.get('phone', '')
            profile.birthday = form.cleaned_data.get('birthday')
            
            # Handle referral code
            referral_code = form.cleaned_data.get('referral_code')
            if referral_code:
                try:
                    referrer_profile = UserProfile.objects.get(referral_code=referral_code.upper())
                    profile.referred_by = referrer_profile
                    
                    # Create referral record
                    Referral.objects.create(
                        referrer=referrer_profile.user,
                        referred_user=user,
                        referral_code_used=referral_code.upper()
                    )
                    
                    # Update referrer's count
                    referrer_profile.referral_count += 1
                    referrer_profile.loyalty_points += 50  # Bonus for referrer
                    referrer_profile.save()
                    
                    # Give new user bonus points
                    profile.loyalty_points = 100  # Welcome bonus!
                    
                    messages.success(request, f'🎉 Welcome! You got 100 bonus points! Your referrer also got 50 points!')
                except UserProfile.DoesNotExist:
                    pass
            else:
                # Regular signup bonus
                profile.loyalty_points = 50
                messages.success(request, f'🎉 Welcome {user.first_name}! You got 50 welcome bonus points!')
            
            profile.save()
            
            # Log user in
            login(request, user)
            
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'loyalty/signup.html', {'form': form})


def login_view(request):
    """
    User login
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}! ✨')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
    else:
        form = LoginForm()
    
    return render(request, 'loyalty/login.html', {'form': form})


def logout_view(request):
    """
    User logout
    """
    logout(request)
    messages.info(request, 'You have been logged out. See you soon! 💕')
    return redirect('index')


@login_required
def dashboard_view(request):
    """
    User dashboard with loyalty info, order history, wishlist
    """
    user = request.user
    profile = user.profile
    
    # Get order statistics
    orders = Order.objects.filter(user=user).order_by('-created_at')
    total_orders = orders.count()
    total_spent = orders.aggregate(total=Sum('final_amount_ksh'))['total'] or 0
    
    # Get recent orders (last 5)
    recent_orders = orders[:5]
    
    # Get wishlist items
    wishlist_items = Wishlist.objects.filter(user=user).order_by('-added_at')[:6]
    
    # Get referral statistics
    referrals_made = Referral.objects.filter(referrer=user)
    successful_referrals = referrals_made.filter(referred_user_made_purchase=True).count()
    
    # Calculate discount percentage
    discount_percentage = profile.get_discount_percentage()
    
    # Get available discounts details
    discounts = []
    if profile.is_student:
        discounts.append({'type': 'Student', 'percentage': 10, 'icon': '🎓'})
    if profile.is_birthday_month():
        discounts.append({'type': 'Birthday Month', 'percentage': 5, 'icon': '🎂'})
    if profile.vip_status:
        discounts.append({'type': 'VIP', 'percentage': 5, 'icon': '👑'})
    
    context = {
        'profile': profile,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
        'wishlist_items': wishlist_items,
        'referrals_count': referrals_made.count(),
        'successful_referrals': successful_referrals,
        'discount_percentage': discount_percentage,
        'discounts': discounts,
        'points_to_next_vip': max(0, 1000 - profile.loyalty_points) if not profile.vip_status else 0,
    }
    
    return render(request, 'loyalty/dashboard.html', context)


@login_required
def profile_settings_view(request):
    """
    Edit user profile and account settings
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'loyalty/profile_settings.html', context)


@login_required
def wishlist_view(request):
    """
    View all wishlist items
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'loyalty/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_type, product_id):
    """
    Add product to wishlist (AJAX)
    """
    if request.method == 'POST':
        # Get the product based on type
        product = None
        wishlist_data = {'user': request.user}
        
        if product_type == 'hairstyle':
            product = get_object_or_404(HairStyle, pk=product_id, available=True)
            wishlist_data['hairstyle'] = product
        elif product_type == 'perfume':
            product = get_object_or_404(Perfume, pk=product_id, available=True)
            wishlist_data['perfume'] = product
        elif product_type == 'clothing':
            product = get_object_or_404(ClothingItem, pk=product_id, available=True)
            wishlist_data['clothing'] = product
        else:
            return JsonResponse({'success': False, 'error': 'Invalid product type'}, status=400)
        
        # Check if already in wishlist
        existing = Wishlist.objects.filter(**wishlist_data).first()
        
        if existing:
            # Remove from wishlist (toggle)
            existing.delete()
            return JsonResponse({
                'success': True,
                'action': 'removed',
                'message': f'{product.name} removed from wishlist'
            })
        else:
            # Add to wishlist
            Wishlist.objects.create(**wishlist_data)
            return JsonResponse({
                'success': True,
                'action': 'added',
                'message': f'💖 {product.name} added to wishlist!'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def remove_from_wishlist(request, wishlist_id):
    """
    Remove item from wishlist
    """
    wishlist_item = get_object_or_404(Wishlist, pk=wishlist_id, user=request.user)
    product_name = wishlist_item.get_product().name
    wishlist_item.delete()
    
    messages.success(request, f'Removed {product_name} from your wishlist')
    return redirect('wishlist')


@login_required
def order_history_view(request):
    """
    View all order history
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Statistics
    total_spent = orders.aggregate(total=Sum('final_amount_ksh'))['total'] or 0
    total_points_earned = orders.aggregate(total=Sum('points_earned'))['total'] or 0
    
    context = {
        'orders': orders,
        'total_spent': total_spent,
        'total_points_earned': total_points_earned,
    }
    
    return render(request, 'loyalty/order_history.html', context)


@login_required
def referrals_view(request):
    """
    View referral statistics and manage referrals
    """
    profile = request.user.profile
    referrals = Referral.objects.filter(referrer=request.user).order_by('-created_at')
    
    # Calculate milestone progress
    milestones = [
        {'count': 3, 'reward': 'Free service (up to KSH 800)', 'achieved': profile.referral_count >= 3},
        {'count': 5, 'reward': '500 bonus points', 'achieved': profile.referral_count >= 5},
        {'count': 10, 'reward': 'VIP Status', 'achieved': profile.referral_count >= 10},
    ]
    
    context = {
        'profile': profile,
        'referrals': referrals,
        'milestones': milestones,
        'referral_url': request.build_absolute_uri('/') + f'?ref={profile.referral_code}',
    }
    
    return render(request, 'loyalty/referrals.html', context)


def check_wishlist_status(request, product_type, product_id):
    """
    Check if product is in user's wishlist (AJAX)
    """
    if not request.user.is_authenticated:
        return JsonResponse({'in_wishlist': False})
    
    wishlist_data = {'user': request.user}
    
    if product_type == 'hairstyle':
        wishlist_data['hairstyle_id'] = product_id
    elif product_type == 'perfume':
        wishlist_data['perfume_id'] = product_id
    elif product_type == 'clothing':
        wishlist_data['clothing_id'] = product_id
    else:
        return JsonResponse({'in_wishlist': False})
    
    in_wishlist = Wishlist.objects.filter(**wishlist_data).exists()
    
    return JsonResponse({'in_wishlist': in_wishlist})

