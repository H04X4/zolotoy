from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('update-order/', views.update_order, name='update_order'),
]