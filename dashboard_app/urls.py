from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile/<str:phone>', views.profile, name='profile'),
    path('edit-profile/<str:phone>', views.edit_profile, name='edit_profile'),
]
