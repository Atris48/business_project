from django.urls import path
from . import views

urlpatterns = [
    path('portfolio-list', views.portfolio, name='portfolio_list')
]