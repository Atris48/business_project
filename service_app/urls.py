from django.urls import path
from . import views

urlpatterns = [
    path('service-list', views.service_list, name='service_list'),
]
