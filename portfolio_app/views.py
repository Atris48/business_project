from django.shortcuts import render
from django.views.generic import ListView


def portfolio(request):
    return render(request, 'portfolio_app/portfolio_list.html')


class PortfolioListView(ListView):
    pass
