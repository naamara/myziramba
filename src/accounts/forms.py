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


class RegisterForm(forms.Form):
	username = forms.CharField(required=False)
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Create password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repeat password"))
	password = None


	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError(
                _('This email is already in use. Please supply a different email.'))
		return self.cleaned_data['email']

	
	def clean(self):

		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(
                    'The two password fields didn\'t match.')
		return self.cleaned_data


	def save(self):
	        """ Creates a new user and account. Returns the newly created user. """

	        '''custom username'''
	        username = self.cleaned_data['username']
	        username, email, password = (username,
	                                     self.cleaned_data['email'],
	                                     self.cleaned_data['password1'])
	        new_user = User.objects.create_user(
	            username=username, email=email, password=password)
	        new_user.save()
	        return new_user


 




class AuthenticationForm(forms.Form):

    """
    A custom form where the identification can be a e-mail address or username.

    """
    username  = forms.CharField(label=_("username "),)

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))

    def __init__(self, *args, **kwargs):
        """ A custom init because we need to change the label if no usernames is used """
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        # Dirty hack, somehow the label doesn't get translated without declaring
        # it again here.
        #self.fields['identification'] = forms.ValidationError(_(u"Email"),_(u"Please supply your email."))

    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        username  = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username  and password:
            user = authenticate(username=username, password=password)


            if user is None:
                raise forms.ValidationError(
                    "Please enter a correct email and password. Note that both fields are case-sensitive.")
        return self.cleaned_data

