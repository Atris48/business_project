import time
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def rate_limit_(max_requests=2, per=60, message=''):
    request_counts = {}

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
                for timestamp in list(request_counts.keys()):
                    if timestamp < current_time - per:
                        del request_counts[timestamp]

                # Get the number of requests made by this IP address in the past "per" seconds
                count = sum(1 for timestamp, ip in request_counts.items() if ip == ip_address)

                # If the IP address has already made "max_requests" requests in the past "per" seconds, return a 429 error response
                if count >= max_requests:
                    retry_after = max(
                        timestamp for timestamp, ip in request_counts.items() if
                        ip == ip_address) + per - current_time
                    messages.error(request, message=f'{message}   {retry_after} ثانیه دیگر مجدد تلاش کنید ')
                    return redirect('login')

                # Otherwise, record the current request and return the wrapped view function
                request_counts[current_time] = ip_address

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


