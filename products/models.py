from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse


class ProductManager(models.Manager):
    def all(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def get_related_products(self, instance):
        qs1 = self.all().filter(categories__in=instance.categories.all())
        qs2 = self.all().filter(default=instance.default)
        return (qs1 | qs2).exclude(id=instance.id).distinct()


class Product(models.Model):
    """
    This is the class based model function that  stores records products for order 
    """
    MY_CHOICES = (
        ('m', 'Construction Materials'),
        ('h', 'Home Decor'),
        ('e', 'Electronic Appliances'),
        ('a', 'Art and Decorations'),
        ('f', 'Furniture'),
        ('s', 'Bed Materials'),
        ('k', 'Kitchen Tools'),
        ('b', 'Bookcase'),
        ('d', 'Drawer'),
        ('c', 'Cabinetry'),
        ('d', 'Dressers'),
        ('o', 'Microwave Oven'),
        ('r', 'Refrigerators'),
        ('v', 'Vaccum Cleaner'),
        ('g', 'Gas Fireplace'),
        ('p', 'Smart Phones'),
       
    )
    section = models.CharField(max_length=1, choices=MY_CHOICES, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
    # slug
    objects = ProductManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """
        This is the function that returns the path for a particular product information
        """
        return reverse('product_detail', args=(self.id,))

    def get_image_url(self):
        """
        This is the function that returns the path for a particular product image 
        """
        img = self.productimage_set.first()
        return img.image.url if img else img


    def save(self, *args, **kwargs):
        """
        This is the function that saves the product record  and creates its variation if it does not exists as Default
        """
        super(Product, self).save(*args, **kwargs)
        if self.variation_set.all().count() == 0:
            Variation.objects.create(product=self, price=self.price, title='Default')
        


class Variation(models.Model):
    """
    This is the class based model function that  stores records of  product variations  
    """
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True) # None is unlimited

    def __unicode__(self):
        return self.title

    def get_price(self):
        """
        return sale price if not None otherwise return prices
        """
        return self.sale_price if self.sale_price else self.price

    def get_absolute_url(self):
        """
        return path of the product
        """
        return self.product.get_absolute_url()

    def get_title(self):
        """
        return title of the product
        """
        return '{0}- {1}'.format(self.product.title, self.title)

    def add_to_cart(self):
        """
        return path  for adding a product to the cart
        """
        return '{0}?item={1}'.format(reverse('create_cart'), self.id)

    def remove_from_cart(self):
        """
        return  function for deleting a product from the cart
        """
        return '{0}&{1}'.format(self.add_to_cart(), 'delete=y')


class ProductImage(models.Model):
    """
    This is the class based model function that  stores records of images uploaded to the products folder of the website 
    """
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products/', null=True)

    def __unicode__(self):
        """
        This is the function that returns title of a product
        """
        return self.product.title


class ProductTrend(models.Model):
    """
    This is the class based model function that  stores records of images uploaded to the products folder of the website 
    """
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products/', null=True)

    def __unicode__(self):
        """
        This is the function that returns title of a product
        """
        return self.product.title




class Category(models.Model):
    """
    This is the class based model function that  stores records of  Category of products 
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        """
        This is the function that returns title of a product
        """
        return self.title

    def get_absolute_url(self):
        """
        This is the function that returns category detail of a particular product
        """
        return reverse('category_detail', kwargs={'slug': self.slug})


class ProductFeatured(models.Model):
    """
    This is the class based model function that  stores records of  uploaded featured products  
    """
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products/featured/')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True, null=True)
    description_right = models.BooleanField(default=False)
    show_price = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        """
        This is the function that returns title of a product
        """
        return self.product.title


class ProductCharged(models.Model):
    """
    This is the class based model function that  stores records of products charged for  during ordering process
    """
    amount = models.PositiveIntegerField()
    source = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    

   