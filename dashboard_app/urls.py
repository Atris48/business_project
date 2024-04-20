from django.urls import path
from . import views
from .admin_views import *

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile/<str:phone>', views.profile, name='profile'),
    path('edit-profile/<str:phone>', views.user_edit_profile, name='edit_profile'),
    path('edit-profile-admin/<str:phone>', admin_edit_profile, name='admin_edit_profile'),
    path('remove-notification/<int:pk>', views.remove_notification, name='remove_notification'),
    path('remove-all-notification', views.remove_all_remove_notification, name='remove_all_remove_notification'),
    path('all-user-list', all_user_list, name='all_user_list'),
    path('filter-user-list', views.filter_user, name='filter_user'),
    path('user-order-list', views.user_order_list, name='user_order_list'),
    path('user-support-order-list', views.user_support_order_list, name='user_support_order_list'),
    path('user-discount-list', views.user_discount_list, name='user_discount_list'),
    path('user-security/<str:phone>', views.user_security, name='user_security'),
    path('user-change-password/<str:phone>', views.user_change_password, name='user_change_password'),
    path('active-two-step-login/<str:phone>', views.active_two_step_login, name='active_two_step_login'),
    path('two-step-check-otp', views.check_two_step_otp, name='check_two_step_otp'),
    path('inactive-two-step-login/<str:phone>', views.inactive_two_step_login, name='inactive_two_step_login'),
    path('inactive-two-step-check-otp', views.check_inactive_otp, name='check_inactive_otp'),
]
# admin urls
urlpatterns += [
    path('admin-create-notification', admin_create_notification, name='create_notification'),
    path('admin-create-announcement', admin_create_announcement, name='admin_create_announcement'),
    path('admin-remove-user/<str:phone>', admin_remove_user, name='admin_remove_user'),
    path('admin-create-user', admin_create_user, name='admin_create_user'),
    path('admin-change-password/<str:phone>', admin_change_password, name='admin_change_password'),
    path('admin-ban-user/<str:phone>', admin_ban_user, name='admin_ban_user'),
    path('admin-order-list', admin_order_list, name='admin_order_list'),
    path('admin-remove-order/<str:pk>', admin_remove_order, name='admin_remove_order'),
    path('admin-edit-order/<str:pk>', admin_edit_order, name='edit_order'),
    path('admin-add-order', admin_add_order, name='admin_add_order'),
    path('admin-support-order-list', admin_support_order_list, name='admin_support_order_list'),
    path('admin-edit-support-orderr/<str:pk>', admin_edit_support_order, name='admin_edit_support_order'),
    path('admin-add-support-orderr', admin_add_support_order, name='admin_add_support_order'),
    path('admin-discount-list', admin_discount_list, name='admin_discount_list'),
    path('admin-remove-discount/<int:pk>', admin_remove_discount, name='admin_remove_discount'),
    path('admin-expire-discount/<int:pk>', admin_expire_discount, name='admin_expire_discount'),
    path('admin-add-discount', admin_add_discount, name='admin_add_discount'),
    path('plans-price-list', plans_price_list, name='plan_price_list'),
    path('change-order-price/<int:pk>', change_website_order_price, name='change_website_order_price'),
    path('change-support-price/<int:pk>', change_support_plan_price, name='change_support_plan_price'),
    path('change-extend-price/<int:pk>', change_extend_plan_price, name='change_extend_plan_price'),
]
