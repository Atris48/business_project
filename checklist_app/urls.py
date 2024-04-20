from django.urls import path
from . import views

urlpatterns = [
    path('checklist/<str:pk>', views.ChecklistView.as_view(), name='checklist'),
    path('admin-update-checklist/<str:pk>', views.ChecklistAdmin.as_view(), name='update_checklist')
]
