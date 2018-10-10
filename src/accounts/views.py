from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect

from .forms import ContactForm, RegisterForm, AuthenticationForm
from products.models import ProductFeatured, Product
import ecommerce.settings as settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.urlresolvers import reverse


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