from django import forms
try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _
import random

attrs_dict = {'required': 'required', 'class': 'span4'}


# from .models import SignUp

class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField()

