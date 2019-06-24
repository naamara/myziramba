from django.conf.urls import url,  include

from . import views
from orders.views import AddressFormView, UserAddressCreateView, ConfirmOrderView, OrdersList


urlpatterns = [
    url(r'^$', views.CartCreateView.as_view(), name='create_cart'),
    url(r'^view/$', views.CartDetailView.as_view(), name='cart_detail'),
    url(r'^deco_detail/$', views.HomeDecoDetailView.as_view(), name='deco_detail'),
    url(r'^const_detail/$', views.const_detail, name='const_detail'),
    url(r'^elect_detail/$', views.elect_detail, name='elect_detail'),
    url(r'^art_detail/$', views.art_detail, name='art_detail'),

    url(r'^viewpay/$', views.CartDetailPayView.as_view(), name='cart_detail_pay'),
    url(r'^charge/$', views.charge, name='charge'),
  
    url(r'^address/$', AddressFormView.as_view(), name='address'),   
    url(r'^address/add/$', UserAddressCreateView.as_view(), name='add_address'),
    url(r'^address/confirm/$', ConfirmOrderView.as_view(), name='confirm_order'),
    url(r'^orders/$', OrdersList.as_view(), name='order_list'),
    #url(r'^accounts/', include('registration.backends.default.urls')),
]

