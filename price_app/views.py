from django.shortcuts import render


def price_list(request):
    return render(request, 'price_app/price-list.html')
