"""
Forms for Her Beauty Hub
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ContactMessage, Booking, OrderMessage, UserProfile


class ContactMessageForm(forms.ModelForm):
    """
    Form for contact page submissions
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': '+123 456 7890'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Subject (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Tell us about your beauty needs or ask us anything...',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'subject': 'Subject (Optional)',
            'message': 'Your Message',
        }

    def clean_email(self):
        """Validate email"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        return email


class BookingForm(forms.ModelForm):
    """
    Form for booking appointments
    """
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'service', 'date', 'time', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': '+123 456 7890'
            }),
            'service': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'type': 'date',
                'required': True
            }),
            'time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'type': 'time'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Any special requests or additional information...',
                'rows': 4
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'service': 'Select Service',
            'date': 'Preferred Date',
            'time': 'Preferred Time (Optional)',
            'message': 'Additional Notes (Optional)',
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with only active services"""
        super().__init__(*args, **kwargs)
        # Only show active services in dropdown
        from .models import Service
        self.fields['service'].queryset = Service.objects.filter(active=True).order_by('order', 'name')
        self.fields['service'].empty_label = "Choose a service..."

    def clean_date(self):
        """Validate booking date is not in the past"""
        from django.utils import timezone
        date = self.cleaned_data.get('date')
        if date:
            if date < timezone.now().date():
                raise forms.ValidationError("Booking date cannot be in the past.")
        return date

    def clean_email(self):
        """Validate and normalize email"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        return email


class OrderMessageForm(forms.ModelForm):
    """
    Form for product order inquiries
    """
    class Meta:
        model = OrderMessage
        fields = ['name', 'email', 'phone', 'quantity', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': '+123 456 7890'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'min': '1',
                'value': '1'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Any special requests or size preferences...',
                'rows': 4
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'quantity': 'Quantity',
            'message': 'Additional Notes (Optional)',
        }


# ============================================================
# AUTHENTICATION & LOYALTY SYSTEM FORMS
# ============================================================

class SignUpForm(UserCreationForm):
    """
    Custom signup form with additional fields
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'your.email@example.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'Last name'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': '+254 XXX XXX XXX (optional)'
        })
    )
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'type': 'date',
            'placeholder': 'Your birthday (for special discounts!)'
        }),
        help_text='Get extra 5% off during your birthday month! 🎂'
    )
    referral_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'SBHXXXXXX (optional)',
            'style': 'text-transform: uppercase;'
        }),
        help_text='Have a referral code? Enter it here for bonus points! 🎁'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'Confirm password'
        })
    
    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please login instead.")
        return email
    
    def clean_referral_code(self):
        """Validate referral code if provided"""
        code = self.cleaned_data.get('referral_code')
        if code:
            code = code.upper()
            if not UserProfile.objects.filter(referral_code=code).exists():
                raise forms.ValidationError("Invalid referral code. Please check and try again.")
        return code


class LoginForm(AuthenticationForm):
    """
    Custom login form with styled fields
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'Username or Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    class Meta:
        model = UserProfile
        fields = ['phone', 'birthday', 'student_id', 'university']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': '+254 XXX XXX XXX'
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'type': 'date'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Your student ID number'
            }),
            'university': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300',
                'placeholder': 'Your university/college name'
            }),
        }
        labels = {
            'phone': 'Phone Number',
            'birthday': 'Birthday',
            'student_id': 'Student ID (for 10% discount)',
            'university': 'University/College',
        }
        help_texts = {
            'student_id': 'Upload your student ID to get verified for 10% off!',
            'birthday': 'Get extra 5% off during your birthday month! 🎂',
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user account details
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition duration-300'
            }),
        }

