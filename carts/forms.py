from django import forms
from .models import Order


    
class OrderForm(forms.ModelForm):
    """
    This is the class based view that displays  all the address necessary information of a user
    """
    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'country', 'postcode', 'town_or_city', 'street_address_1', 'street_address_2', 'county')