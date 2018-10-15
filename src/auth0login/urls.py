from django.conf.urls import url,  include

from . import views
from orders.views import AddressFormView, UserAddressCreateView, ConfirmOrderView, OrdersList

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^', include('social_django.urls', namespace='social')),
    url(r'^login/$', views.Auth0, name='login'),

]













