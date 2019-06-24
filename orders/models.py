from django.conf import settings
from django.db import models

from carts.models import Cart


class UserCheckout(models.Model):
    """
    This is the class based model function that  stores records of a  guest client  
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField('email of guest user', null=True, blank=True)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.user:
            self.email = self.user.email
        super(UserCheckout, self).save(*args, **kwargs)


class UserAddress(models.Model):
    """
    This is the class based model function that  stores records of a  guest client and his or her address 
    """
    BILLING = 'billing'
    SHIPPING = 'shipping'
    ADDRESS_TYPES = (
        (BILLING, 'Billing'),
        (SHIPPING, 'Shipping')
        )
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=100, choices=ADDRESS_TYPES)
    address = models.CharField(max_length=300, null=True, blank=True)
    state =  models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.PositiveIntegerField()
    city = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.address

    def get_full_address(self):
        return '{0}, {1}, {2}'.format(self.address, self.state, self.zipcode)


class Order(models.Model):
    """
    This is the class based model function that  stores records of a  guest client, 
    the items he  or she added to the cart and his or her  shipping address 
    """
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address')
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address')
    shipping_price = models.PositiveIntegerField(default=0)
    order_total = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.cart)

    def save(self, *args, **kwargs):
        """
        This  is the function that first computes the total price of items added to the cart and the shipping
         or delivery price of the items  before saving the whole records transaction to Order Models
        """
        self.order_total = self.cart.cart_price + self.shipping_price
        super(Order, self).save(*args, **kwargs)

    def complete_order(self):
        """
        This is the function that sets the completion status of a user transaaction to 
        complete before  updating  real update takes effect through save function
        """
        self.is_completed = True
        self.save() # save the status of is_completed model field of a record 

