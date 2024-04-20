from django.shortcuts import render, get_object_or_404
from django.views import View
from price_app.models import PriceCategory


class PriceView(View):
    def get(self, request):
        categories = PriceCategory.objects.all()
        return render(request, 'price_app/price-list.html', {'categories': categories})


class PlanCategoryDetail(View):
    def get(self, request, pk):
        category = get_object_or_404(PriceCategory, id=pk)
        plans = category.price_set.all()
        return render(request, 'price_app/plan_category_detail.html', {'plans': plans, 'category': category})
