from turtle import home

from django.urls import path
from . import views
from .views import create_order

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact),
    path('detail/',views.detail),


    path('checkout/',views.checkout),
    path('signup/',views.signup,name='signup'),
    path('signin/', views.signin ,name='signin'),
    path('signout/',views.signout,name= 'signout'),

    path('detail/<int:pk>/', views.detail, name='detail'),

    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    path('add_fav/<int:pk>/', views.add_fav, name='add_fav'),
    path('fav/', views.fav, name='fav'),
    path('remove_fav/<int:pk>/', views.remove_fav, name='remove_fav'),

    path('shop/',views.shop),

    path('change_quantity/<int:pk>/', views.change_quantity, name='change_quantity'),
    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:pk>/', views.add_cart, name='add_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('order_conf/', views.order_conf, name='order_conf'),

    path('create_order/', views.create_order, name='create_order'),
    path('order_history/', views.order_history, name='order_history'),


]

# product_name = models.CharField(max_length=250)