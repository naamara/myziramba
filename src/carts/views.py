from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from . import models
from products import models as product_models
from orders.forms import GuestCheckoutForm, UserAddressForm
from orders.models import UserCheckout, Order, UserAddress
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required
from .forms import MakePaymentForm, OrderForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from products.models import ProductFeatured, Product
stripe.api_key = "sk_test_h6dnQ43clBgHoTYAInAU6sMk"




class HomeDecoDetailView(TemplateView):
    addr_form= None
    template_name = 'home_decor.html'
    

    def get(self, request):
        featured_image = ProductFeatured.objects.first()
        products = Product.objects.all().order_by('?')
     
        home_products = Product.objects.filter(section='h')

        context = {
            "featured_image": featured_image,
            "home_products": home_products,
        }
        return render(request, self.template_name, context)
    
    


def elect_detail(request):
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    elect_products = Product.objects.filter(section='e')

    context = {
        "featured_image": featured_image,
        "elect_products": elect_products,
    }

    if request.GET:
        print  request.GET

    return render(request, "home_decor.html", context)

def art_detail(request):
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    art_products = Product.objects.filter(section='a')

    context = {
        "featured_image": featured_image,
        "art_products": art_products,
    }

    if request.GET:
        print  request.GET

    return render(request, "art_products.html", context)


def const_detail(request):
    featured_image = ProductFeatured.objects.first()
    products = Product.objects.all().order_by('?')
    const_products = Product.objects.filter(section='m')

    context = {
        "featured_image": featured_image,
        "const_products": const_products,
    }

    if request.GET:
        print  request.GET

    return render(request, "const_products.html", context)


class CartCreateView(TemplateView, APIView):
    """ add item to cart request handler """
    template_name = 'carts/view.html'

    @staticmethod
    def _process_cart(item_id, quantity, delete, request):
        cart = None
        is_deleted = False
        if 'cart_id' not in request.session:
            cart = models.Cart.objects.create()
            request.session['cart_id'] = cart.id
        if cart == None:
            cart = models.Cart.objects.get(id=request.session['cart_id'])
        if request.user.is_authenticated():
            cart.user = request.user
            cart.save()
        product_models.Variation.objects.get(id=item_id)
        cart_item, created = models.CartItem.objects.get_or_create(cart=cart, item_id=item_id)
        if created or quantity != 1:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += 1;
        if delete in ['y','yes', 'true', 'True']:
            is_deleted = True
            cart_item.delete()
        else:
            cart_item.save()
        return cart, is_deleted, cart_item

    def get(self, request):
        try:
            item_id = request.GET.get('item')
            quantity = request.GET.get('qty', 1)
            delete = request.GET.get('delete', 'n')
            cart, is_deleted, cart_item = self._process_cart(item_id, int(quantity), delete, request)
            cart_count = cart.total_count
            request.session['cart_count'] = cart_count
            return Response({'success': True,
             'deleted': is_deleted,
              'count': cart.count,
              'item_total': cart_item.item_total,
              'cart_price': cart.cart_price,
              'cart_count': cart_count}, status=status.HTTP_200_OK)
        except Exception as error:
            print error

def charge(request): # new
    if request.method == 'POST':

        cart = models.Cart.objects.get(id=request.session['cart_id'])
        total_price = models.Cart.objects.get(id=request.session['cart_id'])
        
        total_price=total_price.cart_price 
        request.session['total_price']  = total_price
        item_name =cart.items
        new_charge = ProductCharged(
            amount = total_price,
            currency  = request.session['cart_id']
    )   
        new_charge.save()

        print "Token " + request.POST['stripeToken']

        charge = stripe.Charge.create(
            amount=total_price,
            currency='usd',
            description='A Zarambara charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'carts/charge.html')




class CartDetailView(TemplateView):
    addr_form= None
    template_name = 'carts/view.html'
    

    def get(self, request):
        if 'cart_id' not in request.session:
            return redirect('/')
        cart = models.Cart.objects.get(id=request.session['cart_id'])
        total_price = models.Cart.objects.get(id=request.session['cart_id'])
        request.session['cart_id'] 
        total_price=total_price.cart_price 
        request.session['total_price']  = total_price
        addr_form= UserAddressForm
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        return render(request, self.template_name, {'object': cart,'order_form': order_form, 'publishable': settings.STRIPE_PUBLIC_KEY,'payment_form': payment_form,'total_price':total_price})
    
    def get_success_url(self):
        return reverse('cart_checkout')

    def get_user_checkout(self):
        user_checkout_id = self.request.session['user_checkout_id']
        return UserCheckout.objects.get(id=user_checkout_id)

    def post(self, request):
        if not request.user.is_authenticated():
            return redirect('/')
            
        user_checkout, created  = UserCheckout.objects.get_or_create(user=request.user)
        request.session['user_checkout_id'] = user_checkout.id
    
        cart = models.Cart.objects.get(id=request.session['cart_id'])
        total_price = models.Cart.objects.get(id=request.session['cart_id'])
        request.session['cart_id'] 
        total_price=total_price.cart_price 
        request.session['total_price']  = total_price

       
            
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        print payment_form
        
        if  payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            cart = models.Cart.objects.get(id=request.session['cart_id'])
            total_price = models.Cart.objects.get(id=request.session['cart_id'])
            request.session['cart_id'] 
            total_price=total_price.cart_price 
            request.session['total_price']  = total_price
            addr_form= UserAddressForm

            try:
                customer = stripe.Charge.create(
                    amount= int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                subjects = {
                'pending_transaction': 'Pending Transaction',
                'complete_transaction': 'Transaction Complete',
                'user_verification': 'User Pending Verification',
                'user_verification_update': 'User Updated Verification Details',
                'new_user': '',
                'rates_error': 'An error occurred while fetching the rates',
                'server_error': 'Dude your App Just Broke',
                'contact_us': 'New Contact Message',
                }
                msg = EmailMessage('Payement Success', "You have successfully paid", "mandelashaban593@gmail.com", to=[request.user.email,])
                msg.send()
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
            cart = models.Cart.objects.get(id=request.session['cart_id'])
            total_price = models.Cart.objects.get(id=request.session['cart_id'])
            request.session['cart_id'] 
            total_price=total_price.cart_price 
            request.session['total_price']  = total_price
            addr_form= UserAddressForm
            payment_form = MakePaymentForm()
            order_form = OrderForm()
            return render(request, self.template_name, {'object': cart,'order_form': order_form, 'publishable': settings.STRIPE_PUBLIC_KEY,'payment_form': payment_form,'total_price':total_price})
        

class CartDetailPayView(TemplateView):
    addr_form= None
    template_name = 'carts/checkout_pay.html'
    

    def get(self, request):
        if 'cart_id' not in request.session:
            return redirect('/')
        cart = models.Cart.objects.get(id=request.session['cart_id'])
        total_price = models.Cart.objects.get(id=request.session['cart_id'])
        request.session['cart_id'] 
        total_price=total_price.cart_price 
        request.session['total_price']  = total_price
        addr_form= UserAddressForm
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        return render(request, self.template_name, {'object': cart,'order_form': order_form, 'publishable': settings.STRIPE_PUBLIC_KEY,'payment_form': payment_form,'total_price':total_price})
    
    def get_success_url(self):
        return reverse('cart_checkout')

    def get_user_checkout(self):
        user_checkout_id = self.request.session['user_checkout_id']
        return UserCheckout.objects.get(id=user_checkout_id)

    def post(self, request):
        if not request.user.is_authenticated():
            return redirect('/')
            
        user_checkout, created  = UserCheckout.objects.get_or_create(user=request.user)
        request.session['user_checkout_id'] = user_checkout.id
    
        cart = models.Cart.objects.get(id=request.session['cart_id'])
        total_price = models.Cart.objects.get(id=request.session['cart_id'])
        request.session['cart_id'] 
        total_price=total_price.cart_price 
        request.session['total_price']  = total_price

        tomer = stripe.Charge.create(
                    amount= int(total_price * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=9087,
                )

        print "CUSTOMER %s", tomer
            
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        print payment_form
        print order_form
        
        if  payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            cart = models.Cart.objects.get(id=request.session['cart_id'])
            total_price = models.Cart.objects.get(id=request.session['cart_id'])
            request.session['cart_id'] 
            total_price=total_price.cart_price 
            request.session['total_price']  = total_price
            addr_form= UserAddressForm

            try:
                customer = stripe.Charge.create(
                    amount= int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                subjects = {
                'pending_transaction': 'Pending Transaction',
                'complete_transaction': 'Transaction Complete',
                'user_verification': 'User Pending Verification',
                'user_verification_update': 'User Updated Verification Details',
                'new_user': '',
                'rates_error': 'An error occurred while fetching the rates',
                'server_error': 'Dude your App Just Broke',
                'contact_us': 'New Contact Message',
                }
                msg = EmailMessage('Payement Success', "You have successfully paid", "mandelashaban593@gmail.com", to=[request.user.email,])
                msg.send()
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
            cart = models.Cart.objects.get(id=request.session['cart_id'])
            total_price = models.Cart.objects.get(id=request.session['cart_id'])
            request.session['cart_id'] 
            total_price=total_price.cart_price 
            request.session['total_price']  = total_price
            addr_form= UserAddressForm
            payment_form = MakePaymentForm()
            order_form = OrderForm()
            return render(request, self.template_name, {'object': cart,'order_form': order_form, 'publishable': settings.STRIPE_PUBLIC_KEY,'payment_form': payment_form,'total_price':total_price})
        




class CheckoutView(TemplateView, FormMixin):
    model = models.Cart
    template_name = 'carts/checkout_view.html'
    form_class = GuestCheckoutForm

    def get(self, request):
        if 'cart_id' not in request.session:
            return redirect('/')
        cart = models.Cart.objects.get(id=request.session['cart_id'])
        context = {
        'login_form': AuthenticationForm(),
        'object': cart,
        'guest_form': self.get_form(),
        }
        user_checkout = request.session.get('user_checkout_id')
        if not user_checkout:
            if request.user.is_authenticated():
                user_checkout, created  = UserCheckout.objects.get_or_create(user=request.user)
                request.session['user_checkout_id'] = user_checkout.id
        if user_checkout:
            billing_address = request.session.get('billing_address_id')

            if not billing_address:
                return redirect('address')
            if not 'order_id' in request.session:
                order = Order.objects.create(user_id=user_checkout, billing_address_id=billing_address, cart_id=cart.id)
                request.session['order_id'] = order.id
            else:
                order = Order.objects.get(id=request.session['order_id'])
            context['order'] = order
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout, created  = UserCheckout.objects.get_or_create(email=email)
            request.session['user_checkout_id'] = user_checkout.id
            return self.form_valid(form)
        else:
            context = {
                'login_form': AuthenticationForm(),
                'guest_form': form
                }
            return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('cart_checkout')





def payment(request):

    stripe.api_key = "sk_test_h6dnQ43clBgHoTYAInAU6sMk"
    token = request.GET.get['stripeToken'] # Using Flask

    print token
    charge = stripe.Charge.create(
        amount=999,
        currency='usd',
        description='Example charge',
        source=token,
    )

    return render(request, "checkout_pay.html", context)






def checkout2(request):

    cart = models.Cart.objects.get(id=request.session['cart_id'])
    total_price = models.Cart.objects.get(id=request.session['cart_id'])
    
    total_price=total_price.cart_price 
    request.session['total_price']  = total_price
    item_name =cart.items
    new_charge = ProductCharged(
        amount = total_price,
        currency  = request.session['cart_id']
    )


    if request.method == "POST":
        token    = request.POST.get("stripeToken")

    try:
        charge  = stripe.Charge.create(
            amount      = total_price,
            currency    = "usd",
            source      = token,
            description = item_name
        )

        new_car.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        new_charge.save()
        return redirect("thank_you_page")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want




class CheckoutView(TemplateView, FormMixin):
    model = models.Cart
    template_name = 'carts/checkout_view.html'
    form_class = GuestCheckoutForm

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout, created  = UserCheckout.objects.get_or_create(email=email)
            request.session['user_checkout_id'] = user_checkout.id
            return self.form_valid(form)
        else:
            context = {
                'login_form': AuthenticationForm(),
                'guest_form': form
                }
            return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('cart_checkout')
