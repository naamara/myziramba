from django.conf.urls import url,  include

from . import views
from orders.views import AddressFormView, UserAddressCreateView, ConfirmOrderView, OrdersList

urlpatterns = [
   

    url(r'^$', views.home, name='home'), # Path to home view 
    url(r'^dashboard', views.dashboard), # Path to dashboard view 
    url(r'^', include('django.contrib.auth.urls', namespace='auth')), # path to authemtication page of the site


]




