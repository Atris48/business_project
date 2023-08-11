from django.urls import path
from . import views

urlpatterns = [
    path('portfolio-list', views.PortfolioListView.as_view(), name='portfolio_list'),
]