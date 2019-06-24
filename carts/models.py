from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from products import models as product_models


class CartItem(models.Model):
    """
    This is the class based model function for  keeping records of items in to cart
    """
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(product_models.Variation)
    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.item.title

    @property
    def item_name(self):
        """
        This is the function that returns title of the item
        """
        return self.item.get_title()

    def remove(self):
        """
        This is the function that calls a function that initiates removal of items from the cart
        """
        return self.item.remove_from_cart()

    @property
    def item_total(self):
        """
        This is the function that computes that amount of items added to a cart for order
        """
        return self.item.get_price() * self.quantity


class Cart(models.Model):
    """
    This is the class based model function for  keeping records of a user and the items that he adds to the cart
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(product_models.Variation, through=CartItem)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        """
        This is the function that displays the id of cart details
        """
        return str(self.id)

    @property
    def count(self):
        """
        This is the function that returns number of items in a cart
        """
        return self.cartitem_set.count()

    @property
    def cart_price(self):
        """
        This is the function that returns the amount of items in a cart
        """
        total = 0
        for item in self.cartitem_set.all():
            total += item.item_total
        return total

    @property
    def total_count(self):
        """
        This is the function that returns the number of items in a cart
        """
        cart_count = 0
        for item in self.cartitem_set.all():
            cart_count += item.quantity
        return cart_count




class Order(models.Model):
    """
    This is class based model that keeps records of a client that orders for item and his address
    """
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address_1 = models.CharField(max_length=40, blank=False)
    street_address_2 = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    date = models.DateField()

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)