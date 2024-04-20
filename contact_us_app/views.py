import time
from functools import wraps
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from contact_us_app.forms import ContactUsForm
from contact_us_app.models import CompanyInfo


def rate_limit_contact_us(max_requests=2, per=60, message=''):
    request_counts_contact_us = {}

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            # Only apply rate limit to POST requests
            if request.method == 'POST' and not request.user.is_staff:
                # Get the IP address from the incoming request
                ip_address = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
                # Get the current time in seconds
                current_time = int(time.time())

                # Remove any request records that are older than "per" seconds
                for timestamp in list(request_counts_contact_us.keys()):
                    if timestamp < current_time - per:
                        del request_counts_contact_us[timestamp]

                # Get the number of requests made by this IP address in the past "per" seconds
                count = sum(1 for timestamp, ip in request_counts_contact_us.items() if ip == ip_address)

                # If the IP address has already made "max_requests" requests in the past "per" seconds, return a 429 error response
                if count >= max_requests:
                    retry_after = max(
                        timestamp for timestamp, ip in request_counts_contact_us.items() if
                        ip == ip_address) + per - current_time
                    messages.error(request, message=f'{message}   {retry_after} ثانیه دیگر مجدد تلاش کنید ')
                    return redirect('contact_us')

                # Otherwise, record the current request and return the wrapped view function
                request_counts_contact_us[current_time] = ip_address

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


class ContactUs(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'contact_us_app/contact_us.html', {'form': form})

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
