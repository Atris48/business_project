from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from portfolio_app.models import Portfolio, PortfolioCategory


class PortfolioView(View):
    def get(self, request):
        portfolios = Portfolio.objects.order_by('-created_at')
        portfolio_categories = PortfolioCategory.objects.all()
        return render(request, 'portfolio_app/portfolio_list.html',
                      {'portfolios': portfolios, 'portfolio_categories': portfolio_categories})
