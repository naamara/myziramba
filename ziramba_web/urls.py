from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from accounts import views 


urlpatterns = [
    # Examples:
    # Below are the Path to different pages of the websites

    url(r'^contact/$', views.contact, name='contact'),  
    
   

    url(r'^useraddress/$',views.Useraddress, name='useraddress'),
    url(r'^about/$', views.about, name='about'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^singleblog/$', views.singleblog, name='singleblog'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    
    url(r'^products/', include('products.urls')),
    url(r'^cart/', include('carts.urls')),
  
    
    url(r'^', include('auth0login.urls')), # Path to first pages of the websites
    url(r'^accounts/', include('registration.backends.default.urls')),



]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



