from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),  # Новый маршрут
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]