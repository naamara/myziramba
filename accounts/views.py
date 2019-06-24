from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect

from .forms import ContactForm
from orders.forms import GuestCheckoutForm
from products.models import ProductFeatured, Product
import ziramba_web.settings as settings
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

def logout_view(request):
    """
    This is the view function that logs out a user
    """
    logout(request)
    return redirect('home')



def about(request):
    """
    This is the view function that displays information about the website
    """
    return render(request, "about.html", {})

def blog(request):
    """
    This is the view function that displays the blog information of the website
    """
    return render(request, "blog.html", {})

def singleblog(request):
    """
    This is the view function that displays information about each blog of the website
    """
    return render(request, "blog_single.html", {}) 

# Create your views here.



def contact(request):
    """
    This is the view function that displays  form for user to contact the admin of the website which contact information 
    is send to admin gmail 
    """
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'youotheremail@email.com']
        contact_message = "%s: %s via %s"%( 
                form_full_name, 
                form_message, 
                form_email)
        some_html_message = """
        <h1>hello</h1>
        """
        send_mail(subject, 
                contact_message, 
                from_email, 
                to_email, 
                html_message=some_html_message,
                fail_silently=True)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "forms.html", context)






@login_required
def dashboard(request):
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    context = {
        "featured_image": featured_image,
        "products": products
    }
    

    user = request.user
    try:
        auth0user = user.social_auth.get(provider="auth0")
    except:
        auth0User = None

   
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



def Useraddress(request):
    '''
    handles the  payment information of the user   via credit card , mobile money
    @request  request object
    '''
    user_checkout = request.session.get('user_checkout_id')
    useradd = ''
    guest_form = GuestCheckoutForm
    if request.method == 'POST':
      
        type_text = request.POST['type']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        city = request.POST['city']
        user_checkout = request.session.get('user_checkout_id')
        

        if 'cart_id' not in request.session:
            return redirect('/')
        cart = Cart.objects.get(id=request.session['cart_id'])
        context = {
        'login_form': AuthenticationForm(),
        'object': cart,
        'guest_form': guest_form,
        }

        if not user_checkout:
            if request.user.is_authenticated():
                user_checkout, created  = UserCheckout.objects.get_or_create(user=request.user)
                request.session['user_checkout_id'] = user_checkout.id
                useradd = UserAddress(user=user_checkout, type=type_text,state=state,zipcode=zipcode,city=city)
                useradd.save()
        if user_checkout:

            if not 'order_id' in request.session:
                order = Order.objects.create(user_id=user_checkout,cart_id=cart.id)
                request.session['order_id'] = order.id
            else:
                order = Order.objects.get(id=request.session['order_id'])
            context['order'] = order
        return render(request, "carts/checkout_view.html", context)

               
            
            

