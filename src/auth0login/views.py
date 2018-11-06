from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect

from orders.forms import GuestCheckoutForm
from products.models import ProductFeatured, Product
import ecommerce.settings as settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from  orders.models import UserAddress, UserCheckout,  Order
from django.contrib.auth.models import User
from django.shortcuts import redirect
from carts.models import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
import json

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json



@login_required
def dashboard(request):
    user = request.user
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')

    auth0user = user.social_auth.get(provider="auth0")
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }

    return render(request, 'home.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        "featured_image": featured_image,
        "products": products
    })



# Create your views here.
def home(request):
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    context = {
        "featured_image": featured_image,
        "products": products
    }

    if request.GET:
        print  request.GET

    return render(request, "home.html", context)