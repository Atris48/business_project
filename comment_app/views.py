import time
from functools import wraps

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

from comment_app.models import Comment


def rate_limit_comment(max_requests=2, per=60, message=''):
    request_counts_comment = {}

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
                for timestamp in list(request_counts_comment.keys()):
                    if timestamp < current_time - per:
                        del request_counts_comment[timestamp]

                # Get the number of requests made by this IP address in the past "per" seconds
                count = sum(1 for timestamp, ip in request_counts_comment.items() if ip == ip_address)

                # If the IP address has already made "max_requests" requests in the past "per" seconds, return a 429 error response
                if count >= max_requests:
                    retry_after = max(
                        timestamp for timestamp, ip in request_counts_comment.items() if
                        ip == ip_address) + per - current_time
                    messages.error(request, message=f'{message}   {retry_after} ثانیه دیگر مجدد تلاش کنید ')
                    return redirect('resend_active_code')

                # Otherwise, record the current request and return the wrapped view function
                request_counts_comment[current_time] = ip_address

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


class CommentView(View):
    def get(self, request):
        comments = Comment.objects.filter(is_published=True).order_by('-created_at')
        return render(request, 'comment_app/comment_list.html', {'comments': comments})

    @method_decorator(rate_limit_comment(1, 300, 'امکان ارسال نظر نمیباشد'))
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            message = request.POST.get('message')
            Comment.objects.create(user=user, message=message)
            messages.success(request, 'نظر شما ثبت شد')
            return redirect('comment_list')
        else:
            return redirect('index')
