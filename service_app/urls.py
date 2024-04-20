from django.urls import path
from . import views

urlpatterns = [
    path('service-list', views.ServiceView.as_view(), name='service_list'),
]
