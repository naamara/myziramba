from django.conf.urls import url,  include

from . import views
from orders.views import AddressFormView, UserAddressCreateView, ConfirmOrderView, OrdersList

urlpatterns = [
   

    url(r'^$', views.home, name='home'),
    url(r'^dashboard', views.dashboard),
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^', include('social_django.urls', namespace='social')),

]




