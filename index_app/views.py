from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from comment_app.models import Comment
from contact_us_app.forms import ContactUsForm
from contact_us_app.views import rate_limit_contact_us
from order_app.models import SupportPlan
from portfolio_app.models import Portfolio


class Index(View):
    def get(self, request):
        form = ContactUsForm()
        support_plans = SupportPlan.objects.all()
        portfolios = Portfolio.objects.all()
        comments = Comment.objects.all()[:3]
        return render(request, 'index_app/index.html',
                      {'form': form, 'support_plans': support_plans, 'portfolios': portfolios, 'comments': comments})

    @method_decorator(rate_limit_contact_us(1, 300, 'امکان ارسال پیام نمیباشد'))
    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما دریافت شد')
            return redirect('contact_us')
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('contact_us')
