from django.shortcuts import render


def service_list(request):
    return render(request, 'service_app/service_list.html')
