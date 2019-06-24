from django.contrib import admin

import models

# Register your models here.
class CartItemInline(admin.TabularInline):
	"""
	This class based function ensures that CartItem model appears within django admin dashboard
	"""
	
	model = models.CartItem
    


class CartAdmin(admin.ModelAdmin):
	"""
	This class based function ensures that Cart model appears within django admin dashboard
	"""
	inlines = (CartItemInline,)
	class Meta:
		model = models.Cart
        
    
    


admin.site.register(models.Cart, CartAdmin)