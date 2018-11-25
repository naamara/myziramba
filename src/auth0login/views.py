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
    const_products = Product.objects.filter(section='m')
    home_products = Product.objects.filter(section='h')
    elect_products = Product.objects.filter(section='e')
    art_products = Product.objects.filter(section='a')
    furn_products = Product.objects.filter(section='f')
    bed_products = Product.objects.filter(section='s')
    kitch_products = Product.objects.filter(section='k')
    book_products = Product.objects.filter(section='b')
    drawer_products = Product.objects.filter(section='d')
    cabin_products = Product.objects.filter(section='c')
    dress_products = Product.objects.filter(section='Dressers')
    Oven_products = Product.objects.filter(section='o')
    ref_products = Product.objects.filter(section='r')
    vac_products = Product.objects.filter(section='v')
    gas_products = Product.objects.filter(section='g')
    smart_products = Product.objects.filter(section='p')

    context = {
        "featured_image": featured_image,
        "products": products,
        "const_products": const_products,
        "home_products": home_products,
        "elect_products": elect_products,
        "art_products": art_products,
        "furn_products": furn_products,
        "bed_products": bed_products,
        "book_products": book_products,
        "kitch_products": kitch_products,
        "drawer_products": drawer_products,
        "cabin_products": cabin_products,
        "dress_products": dress_products,
        "Oven_products": Oven_products,
        "ref_products": ref_products,
        "vac_products": vac_products,
        "gas_products": gas_products,
        "smart_products":smart_products
    }

    if request.GET:
        print  request.GET

    return render(request, "home.html", context)