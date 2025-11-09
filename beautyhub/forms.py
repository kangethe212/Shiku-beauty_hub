"""
Forms for Her Beauty Hub
"""
from django import forms
from .models import ContactMessage, Booking, OrderMessage


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

