from django.urls import path
from . import views

urlpatterns = [
    path('comment-list', views.comment_list, name='comment_list'),
]
