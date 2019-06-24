from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from orders.models import UserAddress


class GuestCheckoutForm(forms.Form):
    """
    This is the class based view function that validates the email address of 
    a user to ensure that it is not a duplicate email
    """
    email = forms.EmailField()
    email2 = forms.EmailField(label='confirm email')

    def clean_email2(self):
        """
        This is the function that only returns success message after a user's email address does not exists
        """
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email == email2:
            is_user_exists = User.objects.filter(email=email).exists()
            if is_user_exists:
                raise forms.ValidationError(
                    'User already exists. Please login instead')
            return True
        else:
            raise forms.ValidationError('please confirm email')


class AddressForm(forms.Form):
    """
    This is the class based view function that is used for displaying address fields for selection of a cient
    """
    billing_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(type=UserAddress.BILLING),
                                             empty_label=None, widget=forms.RadioSelect)
    shipping_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(type=UserAddress.SHIPPING),
    										 empty_label=None, widget=forms.RadioSelect)


class UserAddressForm(forms.ModelForm):
    """
    This is the class based view function that displays the user address fields 
    """
    class Meta:
        model = UserAddress
        fields = ('type', 'address', 'state', 'zipcode', 'city')
