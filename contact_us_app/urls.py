from django.urls import path
from . import views

urlpatterns = [
    path('contact-us', views.contact_us, name='contact_us'),
    path('faq', views.frequently_asked_questions, name='frequently_asked_questions'),
]
