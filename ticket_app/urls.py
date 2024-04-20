from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:phone>', views.ChatView.as_view(), name='chat'),
    path('create-chat', views.CreateChatView.as_view(), name='create_chat'),
    path('chat-list', views.ChatListView.as_view(), name='chat_list'),
    path('admin-clear-chat/<int:pk>', views.AdminClearChat.as_view(), name='admin_clear_chat'),
]
