from django.urls import path
from . import views

urlpatterns = [
    path('price-list', views.price_list, name='price_list'),
]