from django.shortcuts import render


def contact_us(request):
    return render(request, 'contact_us_app/contact_us.html')


def frequently_asked_questions(request):
    return render(request, 'contact_us_app/faq.html')
