from django.urls import path
from . import views

urlpatterns = [
    path('price-list', views.PriceView.as_view(), name='price_list'),
    path('plan-category-detail/<int:pk>', views.PlanCategoryDetail.as_view(), name='plan_category_detail'),
]
