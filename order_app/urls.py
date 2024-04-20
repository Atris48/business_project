from django.urls import path
from . import views
from .zarin_pal import *
from .support_views import *

urlpatterns = [
    path('order-detail', views.OrderDetail.as_view(), name='order_detail'),
    path('order-detail-prit/<str:pk>', views.OrderDetailPrint.as_view(), name='order_detail_print'),
    path('add-order', views.AddOrder.as_view(), name='add_order'),
    path('remove-order/<str:pk>', views.RemoveOrder.as_view(), name='remove_order'),
    path('apply-discount', views.ApplyDiscount.as_view(), name='apply_discount'),
    path('order-add-note', views.OrderAddNote.as_view(), name='order_add_note'),
    path('send-request/<str:pk>', send_request, name='send_request'),
    path('verify-pay', verify, name='verify_pay'),
]

urlpatterns += [
    path('support-plans', SupportView.as_view(), name='support'),
    path('support-detail', SupportDetail.as_view(), name='support_detail'),
    path('support-order-remove/<str:pk>', RemoveSupportOrder.as_view(), name='support_remove'),
    path('support-order-add-note', SupportOrderAddNote.as_view(), name='support_add_note'),
    path('support-order-detail-prit/<str:pk>', SupportOrderDetailPrint.as_view(),
         name='support_order_detail_print'),
    path('support-apply-discount', SupportApplyDiscount.as_view(), name='support_apply_discount'),
    path('support-send-request/<str:pk>', support_send_request, name='support_send_request'),
    path('support-verify-pay', support_verify, name='support_verify'),
    path('extend-support-order/<str:pk>', ExtendSupportOrder.as_view(), name='extend_support_order'),
    path('extend-support-send-request/<str:pk>', extend_support_send_request, name='extend_support_send_request'),
    path('extend-support-order-pay', extend_support_verify_pay, name='extend_support_order'),
]
