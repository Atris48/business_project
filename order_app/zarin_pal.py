import json
import jdatetime
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from sms.sms import send_sms
from .models import *
from django.contrib import messages
from .views import set_service_status, set_order_status

ZP_API_REQUEST = f"https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 1000  # Rial / Required
description = " پرداخت "  # Required
CallbackURL = 'http://127.0.0.1:8000/verify-pay'


def send_request(request, pk):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, tracking_code=pk)
            if order.applied_discount_code:
                if Discount.objects.filter(code=order.applied_discount_code).exists():
                    discount_code = Discount.objects.get(code=order.applied_discount_code)
                    if discount_code.is_expired:
                        order.total_price = order.total_items_price()
                        order.save()
                        messages.error(request, 'کد تخفیف منقضی شده است')
                        return redirect('order_detail')
                else:
                    order.is_discount_applied = None
                    order.applied_discount_code = None
                    for item in order.items.all:
                        total = 0
                        total += item.price
                    order.save()
                    messages.error(request, 'کد تخفیف وارد شده منقضی شده است')
                    return redirect('order_detail')
            request.session['order_id'] = order.id
            price = (order.total_price * 9) / 100
            tax_price = order.total_price + price
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": (tax_price * 10),
                "description": description,
                "callback_url": CallbackURL,
            }
            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            data = json.dumps(req_data)
            req = requests.post(ZP_API_REQUEST, data=data, headers=req_header, timeout=10)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                messages.error(request, message=e_message)
                return redirect('order_detail')
        except:
            messages.error(request, 'مشکلی در سیستم پرداخت بوجود آمده است')
    return redirect('index')


def verify(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    t_authority = request.GET.get('Authority')
    if request.GET.get('Status') == 'OK':
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total_price,
            "authority": t_authority,
        }
        data = json.dumps(req_data)
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if len(response.json()['errors']) == 0:
            t_status = response.json()['data']['code']
            if t_status == 100:
                order.pay_at = jdatetime.datetime.now()
                order.is_paid = True
                order.save()
                send_sms(order.user.phone, 'confirmorder', parm1=order.user.phone)
                send_sms('0903377992-09120993133', 'neworder', parm1=order.user.phone)
                messages.success(request, "سفارش شما با موفقیت ثبت شد!")
                return redirect('dashboard')
            elif t_status == 101:
                messages.error(request, 'تراکنش ناموفق بود')
                return redirect("order_detail")
            else:
                messages.error(request, 'تراکنش ناموفق بود')
                return redirect("order_detail")
        else:
            messages.error(request, 'تراکنش ناموفق بود')
            return redirect("order_detail")
    else:
        messages.error(request, 'تراکنش شما انجام نشد مجدد تلاش کنید')
        return redirect("order_detail")


SupportCallbackURL = 'http://127.0.0.1:8000/support-verify-pay'


def support_send_request(request, pk):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Support, tracking_code=pk)
            if order.applied_discount_code:
                if Discount.objects.filter(code=order.applied_discount_code).exists():
                    discount_code = Discount.objects.get(code=order.applied_discount_code)
                    if discount_code.is_expired:
                        set_service_status(order, order.plan.price)
                        messages.error(request, 'کد تخفیف منقضی شده است')
                        return redirect('order_detail')
                else:
                    set_service_status(order, order.plan.price)
                    messages.error(request, 'کد تخفیف وارد شده منقضی شده است')
                    return redirect('order_detail')
            request.session['order_id'] = order.id
            price = (order.price * 9) / 100
            tax_price = order.price + price
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": (tax_price * 10),
                "description": description,
                "callback_url": SupportCallbackURL,
            }
            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            data = json.dumps(req_data)
            req = requests.post(ZP_API_REQUEST, data=data, headers=req_header, timeout=10)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                messages.error(request, message=e_message)
                return redirect('order_detail')
        except:
            messages.error(request, 'مشکلی در سیستم پرداخت بوجود آمده است')
    return redirect('index')


def support_verify(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Support, id=order_id)
    t_authority = request.GET.get('Authority')
    if request.GET.get('Status') == 'OK':
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.price,
            "authority": t_authority,
        }
        data = json.dumps(req_data)
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if len(response.json()['errors']) == 0:
            t_status = response.json()['data']['code']
            if t_status == 100:
                order.pay_at = jdatetime.datetime.now()
                order.is_paid = True
                if order.plan.period == 'ماهانه':
                    day = 30
                elif order.plan.period == 'سه ماه':
                    day = 90
                else:
                    day = 180
                expiration_date = jdatetime.datetime.now() + jdatetime.timedelta(days=day)
                order.expiration_date = expiration_date
                order.save()
                send_sms(order.user.phone, 'confirmsuppurt', parm1=order.user.phone)
                send_sms('09033779952-09120993133', 'newsupport', parm1=order.user.phone)
                messages.success(request, "سفارش شما با موفقیت ثبت شد!")
                return redirect('dashboard')
            elif t_status == 101:
                messages.error(request, 'تراکنش ناموفق بود')
                return redirect("support_detail")
            else:
                messages.error(request, 'تراکنش ناموفق بود')
                return redirect("support_detail")
        else:
            messages.error(request, 'تراکنش ناموفق بود')
            return redirect("support_detail")
    else:
        messages.error(request, 'تراکنش شما انجام نشد مجدد تلاش کنید')
        return redirect("support_detail")


ExtendSupportCallbackURL = 'http://127.0.0.1:8000/extend-support-verify-pay'


def extend_support_send_request(request, pk):
    if request.method == 'POST':
        support_order = get_object_or_404(Support, tracking_code=pk)
        if support_order.is_paid:
            now = jdatetime.datetime.now()
            different_time = support_order.expiration_date - now
            plan_id = request.POST.get('plan_id')
            if not plan_id:
                messages.error(request, 'زمان تمدید را انتخاب کتید')
                return redirect('extend_support_order', pk)
            plan = get_object_or_404(ExtendSupportPlan, id=plan_id)
            if different_time.days > 0 and different_time.days < 4:
                request.session['order_id'] = support_order.id
                price = (plan.price * 9) / 100
                tax_price = plan.price + price
                req_data = {
                    "merchant_id": settings.MERCHANT,
                    "amount": (tax_price * 10),
                    "description": description,
                    "callback_url": ExtendSupportCallbackURL,
                }
                req_header = {
                    "accept": "application/json",
                    "content-type": "application/json"
                }
                data = json.dumps(req_data)
                req = requests.post(ZP_API_REQUEST, data=data, headers=req_header, timeout=10)
                authority = req.json()['data']['authority']
                if len(req.json()['errors']) == 0:
                    return redirect(ZP_API_STARTPAY.format(authority=authority))
                else:
                    e_code = req.json()['errors']['code']
                    e_message = req.json()['errors']['message']
                    messages.error(request, message=e_message)
                    return redirect('extend_support_order', pk)
            elif different_time.days < 0 and different_time.days > -5:
                request.session['order_id'] = support_order.id
                price = (plan.price * 9) / 100
                tax_price = plan.price + price
                req_data = {
                    "merchant_id": settings.MERCHANT,
                    "amount": (tax_price * 10),
                    "description": description,
                    "callback_url": SupportCallbackURL,
                }
                req_header = {
                    "accept": "application/json",
                    "content-type": "application/json"
                }
                data = json.dumps(req_data)
                req = requests.post(ZP_API_REQUEST, data=data, headers=req_header, timeout=10)
                authority = req.json()['data']['authority']
                if len(req.json()['errors']) == 0:
                    return redirect(ZP_API_STARTPAY.format(authority=authority))
                else:
                    e_code = req.json()['errors']['code']
                    e_message = req.json()['errors']['message']
                    messages.error(request, message=e_message)
                    return redirect('extend_support_order', pk)
            elif different_time == 0:
                request.session['order_id'] = support_order.id
                price = (plan.price * 9) / 100
                tax_price = plan.price + price
                req_data = {
                    "merchant_id": settings.MERCHANT,
                    "amount": (tax_price * 10),
                    "description": description,
                    "callback_url": SupportCallbackURL,
                }
                req_header = {
                    "accept": "application/json",
                    "content-type": "application/json"
                }
                data = json.dumps(req_data)
                req = requests.post(ZP_API_REQUEST, data=data, headers=req_header, timeout=10)
                authority = req.json()['data']['authority']
                if len(req.json()['errors']) == 0:
                    return redirect(ZP_API_STARTPAY.format(authority=authority))
                else:
                    e_code = req.json()['errors']['code']
                    e_message = req.json()['errors']['message']
                    messages.error(request, message=e_message)
                    return redirect('extend_support_order', pk)
            else:
                messages.error(request, 'شما تنها 7 روز مانده به اتمام پلن قادر به تمدید هستید')
                return redirect('dashboard')
        else:
            messages.error(request, 'ابتدا صورت حساب خود را پرداخت کنید')
            return redirect('support_detail')
    return redirect('index')


def extend_support_verify_pay(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Support, id=order_id)
    t_authority = request.GET.get('Authority')
    if request.GET.get('Status') == 'OK':
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.price,
            "authority": t_authority,
        }
        data = json.dumps(req_data)
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if len(response.json()['errors']) == 0:
            t_status = response.json()['data']['code']
            if t_status == 100:
                order.pay_at = jdatetime.datetime.now()
                order.is_paid = True
                if order.plan.period == 'ماهانه':
                    day = 30
                elif order.plan.period == 'سه ماه':
                    day = 90
                else:
                    day = 180
                expiration_date = jdatetime.datetime.now() + jdatetime.timedelta(days=day)
                order.expiration_date = expiration_date
                order.is_expiration = False
                order.save()
                send_sms('09033779952-09120993133', 'newsupportextend', parm1=order.user.phone)
                messages.success(request, "پلن شما با موفقیت تمدید شد!")
                return redirect('dashboard')
            elif t_status == 101:
                messages.error(request, 'تراکنش ناموفق بود')
                return redirect("support_detail")
            else:
                messages.error(request, 'تراکنش ناموفق بود')
                return redirect("support_detail")
        else:
            messages.error(request, 'تراکنش ناموفق بود')
            return redirect("support_detail")
    else:
        messages.error(request, 'تراکنش شما انجام نشد مجدد تلاش کنید')
        return redirect("support_detail")
