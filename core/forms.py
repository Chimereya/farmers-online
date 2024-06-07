from django import forms
from .models import BillingAddress

        
        
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name'
    }))
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    street_address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Street Address'
    }))
    apartment_address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment Address'
    }))
    zip = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ZIP Code'
    }))

    
    