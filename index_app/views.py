from django.contrib import messages
from django.shortcuts import render


def index(request):
    return render(request, 'index_app/index.html')
