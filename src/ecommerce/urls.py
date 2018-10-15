from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Examples:
    url(r'^$', 'accounts.views.home', name='home'),
    url(r'^contact/$', 'accounts.views.contact', name='contact'),
    url(r'^register/$', 'accounts.views.register', name='register'),
    url(r'^signin/$', 'accounts.views.signin', name='signin'),

    url(r'^completeauth0/$', 'accounts.views.completeauth0', name='completeauth0'),
    url(r'^useraddress/$', 'accounts.views.Useraddress', name='useraddress'),
    url(r'^about/$', 'ecommerce.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^cart/', include('carts.urls')),
    url(r'^auth0login/', include('auth0login.urls')),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



