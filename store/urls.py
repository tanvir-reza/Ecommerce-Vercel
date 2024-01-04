from django.urls import path,include
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

urlpatterns = [
    path('', index, name='home'),
    path('product/<slug:slug>', product_detail, name='product'),
    path('search/<slug:slug>', categoryProducts, name='category'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


