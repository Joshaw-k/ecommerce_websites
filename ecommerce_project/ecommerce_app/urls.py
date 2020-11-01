from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index,name='index'),
    path('cart/',views.cart,name='cart'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('checkout/',views.checkout,name='checkout'),
    path('updateuseritem/',views.updateuseritem,name='updateuseritem'),
    path('checkout/processorder/',views.processorder,name='processorder'),
]