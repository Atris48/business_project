from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from checklist_app.models import Checklist
from order_app.models import Order, Discount
from price_app.models import Price
from uuid import uuid4
from contact_us_app.models import CompanyInfo


def calculate_discount_price(discount, price):
    discounted_price = (price * discount) / 100
    return price - discounted_price


def set_order_status(order, price):
    order.applied_discount_code = None
    order.is_discount_applied = False
    order.total_price = price
    order.save()


def set_service_status(support, price):
    support.applied_discount_code = None
    support.is_discount_applied = False
    support.total_price = price
    support.save()


class AddOrder(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if Order.objects.filter(user=request.user).exists():
                for item in Order.objects.filter(user=request.user).all():
                    if item.is_paid == False:
                        messages.error(request, 'ابتدا صورت حساب قبلی خود را پرداخت یا حذف کنید')
                        return redirect('order_detail')
                category = request.POST.get('category')
                plan_name = request.POST.get('plan_name')
                if Price.objects.filter(category__title=category, name=plan_name).exists():
                    plan = Price.objects.get(category__title=category, name=plan_name)
                    unique_code = uuid4()
                    tracking_code = str(unique_code)[:12]
                    order = Order.objects.create(user=user, total_price=plan.price, plan_type=plan.name,
                                                 plan_category=category,
                                                 tracking_code=tracking_code)
                    Checklist.objects.create(order=order)
                    messages.success(request, 'پلن به صورتحساب شما اضافه شد')
                    return redirect('order_detail')
                else:
                    messages.error(request, 'پلن یافت نشد')
                    return redirect('price_list')
            else:
                category = request.POST.get('category')
                plan_name = request.POST.get('plan_name')
                plan = Price.objects.get(category__title=category, name=plan_name)
                unique_code = uuid4()
                tracking_code = str(unique_code)[:12]
                order = Order.objects.create(user=user, total_price=plan.price, plan_type=plan.name,
                                             plan_category=category,
                                             tracking_code=tracking_code)
                Checklist.objects.create(order=order)
                messages.success(request, 'پلن به صورت حساب اضافه شد')
                return redirect('order_detail')
        else:
            return redirect('index')


class RemoveOrder(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, tracking_code=pk)
        order.delete()
        messages.success(request, 'صورت حساب شما حذف شد')
        return redirect('price_list')


class OrderDetail(View):
    def get(self, request):
        if request.user.is_authenticated:
            if Order.objects.filter(user__phone=request.user.phone, is_paid=False).exists():
                order = Order.objects.get(user__phone=request.user.phone, is_paid=False)
                company_info = CompanyInfo.objects.first()
                price = Price.objects.get(category__title=order.plan_category, name=order.plan_type)
                if order.is_discount_applied:
                    if Discount.objects.filter(code=order.applied_discount_code).exists():
                        discount = Discount.objects.get(code=order.applied_discount_code)
                        if discount.is_expired:
                            set_order_status(order, price.price)
                            messages.error(request, 'کد تخفیف منقضی شده است')
                            return redirect('order_detail')
                        else:
                            discount_price = (price.price * discount.percentage) / 100
                    else:
                        set_order_status(order, price.price)
                        messages.error(request, 'کد تخفیف منسوخ شده است')
                        return redirect('order_detail')
                else:
                    discount_price = 0
                return render(request, 'order_app/order_detail.html',
                              {"order": order, "info": company_info, "price": price,
                               "discount_price": int(discount_price)})
            else:
                messages.error(request, 'شما صورت حسابی ندارید')
                return redirect('price_list')
        else:
            return redirect('login')


class ApplyDiscount(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            code = request.POST.get('code')
            for order in Order.objects.filter(user=user).all():
                if order.is_paid == False:
                    if order.is_discount_applied:
                        messages.error(request, 'کد تخفیف اعمال شده است')
                        return redirect('order_detail')
                    if Discount.objects.filter(code=code).exists():
                        discount = Discount.objects.get(code=code)
                        if not discount.is_expired:
                            discounted_price = calculate_discount_price(discount.percentage, order.total_price)
                            order.total_price = discounted_price
                            order.applied_discount_code = code
                            order.is_discount_applied = True
                            order.save()
                            messages.success(request, 'کد تخفیف اعمال شد')
                            return redirect('order_detail')
                        else:
                            messages.error(request, 'کد تخفیف منقضی شده است')
                            return redirect('order_detail')
                    else:
                        messages.error(request, 'کد تخفیف یافت نشد')
                        return redirect('order_detail')
            return redirect('price_list')
        else:
            return redirect('login')


class OrderAddNote(View):
    def post(self, request):
        if request.user.is_authenticated:
            note = request.POST.get('note')
            if Order.objects.filter(user=request.user).exists():
                orders = Order.objects.filter(user=request.user).all()
                for order in orders:
                    if order.is_paid == False:
                        if note:
                            order.note = note
                            order.save()
                            messages.success(request, 'یادداشت شما به صورتحساب اضافه شد')
                            return redirect('order_detail')
                        else:
                            messages.error(request, 'یادداشت خود را به درستی وارد کنید')
                            return redirect('order_detail')
                return redirect('price_list')
            else:
                return redirect('dashboard')
        else:
            redirect('login')


class OrderDetailPrint(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, tracking_code=pk)
            company_info = CompanyInfo.objects.first()
            price = Price.objects.get(category__title=order.plan_category, name=order.plan_type)
            if order.is_discount_applied:
                if Discount.objects.filter(code=order.applied_discount_code).exists():
                    discount = Discount.objects.get(code=order.applied_discount_code)
                    if discount.is_expired:
                        set_order_status(order, price.price)
                        messages.error(request, 'کد تخفیف منقضی شده است')
                        return redirect('order_detail')
                    else:
                        discount_price = (price.price * discount.percentage) / 100
                else:
                    set_order_status(order, price.price)
                    messages.error(request, 'کد تخفیف منسوخ شده است')
                    return redirect('order_detail')
            else:
                discount_price = 0
            return render(request, 'order_app/order_detail_print.html',
                          {"order": order, "info": company_info, "price": price,
                           "discount_price": int(discount_price)})
        else:
            return redirect('login')
