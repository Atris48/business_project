from django.shortcuts import render
from django.views import View
from service_app.models import ServiceCategory


class ServiceView(View):
    def get(self, request):
        service_categories = ServiceCategory.objects.all()
        return render(request, 'service_app/service_list.html', {'service_categories': service_categories})
