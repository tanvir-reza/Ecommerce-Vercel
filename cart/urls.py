from django.urls import path,include
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

urlpatterns = [
    path('add-cart/', cart_add, name='add_to_cart'),
    path('del-cart/', cart_del, name='delete_cart'),
    path('', cart_summery, name='cart-summery'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-fail/', payment_fail, name='payment_fail'),
    path('payment-status/', payment_status, name='payment_status'),

    path('pdf/', download_pdf, name='pdf'),
   
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)