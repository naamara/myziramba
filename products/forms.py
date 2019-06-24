from django import forms

import models


class VariationInventoryForm(forms.ModelForm):
	"""
    This is the class based view function that for variations of item that a client  wants to order 
    """
	class Meta:
		model = models.Variation
		fields = ('title', 'price', 'sale_price', 'inventory', 'active')


VariationInventoryFormSet = forms.models.modelformset_factory(models.Variation, form=VariationInventoryForm, extra=1)