from django.urls import path,include
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('update-profile/', update_profile, name='update_profile'),
    path('orders/', ordersView, name='orders'),
    path('deshboard/', dashboard, name='deshboard'),
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('success/', userSuccess,),
]
