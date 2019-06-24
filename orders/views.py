from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.edit import FormView, CreateView
from django.core.urlresolvers import reverse

from .forms import AddressForm, UserAddressForm
from .models import UserAddress, UserCheckout, Order
from products.mixins import LoginRequiredMixin


"""
The below view functions are important for purpose of delivery of the products to its destinations. 
We shall be using them as we proceed with the projects. But all are planned for 
"""
class UserAddressCreateView(CreateView):
    """
    This view function handles the location details of a client

    """
    form_class = UserAddressForm
    template_name = 'forms.html'
    
    def get_success_url(self):
        return reverse('cart_checkout')

    def get_user_checkout(self):
        """
        This function displays the details of a guest user of the website 
        """
        user_checkout_id = self.request.session['user_checkout_id']
        return UserCheckout.objects.get(id=user_checkout_id)

    def form_valid(self, form, *args, **kwargs):
        """
        This is the function that makes sure the details of a user in the form are all in the right form of the fields
        """
        form.instance.user = self.get_user_checkout()
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


class AddressFormView(FormView):
    """
    This is the class based view that handles all the address function of the user ,
    User location to which goods are to be deliverd
    """
    form_class = AddressForm
    template_name = 'orders/address_select.html'

    def dispatch(self, request, *args, **kwargs):
        """
        This is the function that ensures that a user enters the address to which his goods are to be shipped 
        """
        b_address, s_address = self.get_address()
        if not (b_address.exists() and s_address.exists()):
            messages.success(self.request, 'Please add an address before continuing')
            return redirect('add_address')
        return super(AddressFormView, self).dispatch(request, *args, **kwargs)

    def get_address(self, *args, **kwargs):
        """
        This is the function that retrives and returns the address information of a client
        """
        user_checkout  = self.request.session['user_checkout_id']
        b_address = UserAddress.objects.filter(
            type=UserAddress.BILLING, user_id=user_checkout)
        s_address = UserAddress.objects.filter(
            type=UserAddress.SHIPPING, user_id=user_checkout)
        return b_address, s_address

    def get_form(self):
        """
        This is the function that  retrives and returns the address information of a client
        """
        form = super(AddressFormView, self).get_form()
        b_address, s_address = self.get_address()
        form.fields['billing_address'].queryset = b_address
        form.fields['shipping_address'].queryset = s_address
        return form

    def form_valid(self, form, *args, **kwargs):
        """
        This is the function that ensures that the address informations are valid 
        and it also stores the address information of the user in django session variables for later usage
        """
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        self.request.session['billing_address_id'] = billing_address.id
        self.request.session['shipping_address_id'] = shipping_address.id
        return super(AddressFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        """
        This is function that returns the success url of checking out a good
        """
        return reverse('cart_checkout')


class ConfirmOrderView(View):
    """"
    This is the class based view function that handles the completion of 
    ordering for items online
    """
    def post(self, request):
        """"
        This is the function that destroys the orders of a client after its completion.
        It redirects the client to order for more items , incase he or she denies to complete the order
        """
        order = Order.objects.get(id=request.session['order_id'])
        if request.POST.get('complete_order'):
            order.complete_order()
            del request.session['order_id']
            del request.session['cart_id']
            del request.session['cart_count']
        return redirect('/')


class OrdersList(LoginRequiredMixin, ListView):
    """
    This is the function that displays the complete list of items and their details a client ordrs
    """
    model = Order
    template_name = 'orders/orders_list.html'


    def get_queryset(self):
        return Order.objects.filter(user__user=self.request.user)
