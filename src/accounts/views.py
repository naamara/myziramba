from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect

from .forms import ContactForm, RegisterForm, AuthenticationForm
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


# Create your views here.
def home(request):
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    context = {
        "featured_image": featured_image,
        "products": products
    }

    return render(request, "home.html", context)


def contact(request):
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



def register(request):
    title = 'Register'
    title_align_center = True
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    context = {
        "featured_image": featured_image,
        "products": products
    }


    post_values = request.POST.copy()
   
    form = RegisterForm(post_values)
    if form.is_valid():
        user = form.save()

        form_username= form.cleaned_data.get("username")
        form_email = form.cleaned_data.get("email")
        form_password = form.cleaned_data.get("password1")
        form_cpassword = form.cleaned_data.get("password2")
        # print email, message, full_name
        subject = 'Site Registration form'

        user = authenticate(username=form_email, password=form_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, "home.html", context)

    
    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "register.html", context)




def signin(request):
    '''
    handles the signup page
    @request  request object
    '''
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    context = {
        "featured_image": featured_image,
        "products": products
    }

    auth_form = AuthenticationForm()
    form = AuthenticationForm()
    if request.method == 'POST':
      
        username = request.POST['username']
        password = request.POST['password']
           
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, "home.html", context)

            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, "home.html", context)
            # extradata =
    return render_view(request, 'login.html', {})




def Useraddress(request):
    '''
    handles the signup page
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

               
            
            

