from django.shortcuts import render


def about_us(request):
    return render(request, 'about_app/about.html')
