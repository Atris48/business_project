from django.urls import path
from . import views

urlpatterns = [
    path('comment-list', views.CommentView.as_view(), name='comment_list'),
]
