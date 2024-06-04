from django import forms
from .models import BillingAddress

        
        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['full_name', 'email', 'street_address', 'apartment_address', 'zip']
    
    