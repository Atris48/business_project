from uuid import uuid4
import jdatetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from contact_us_app.models import CompanyInfo
from order_app.models import SupportPlan, Support, Discount, ExtendSupportPlan
from order_app.views import set_service_status, calculate_discount_price


class SupportView(View):
    def get(self, request):
        support_plans = SupportPlan.objects.all()
        return render(request, 'order_app/support_plan.html', {'plans': support_plans})

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            support_plan_id = request.POST.get('plan_id')
            support_plan = get_object_or_404(SupportPlan, id=support_plan_id)

            if Support.objects.filter(user=user, is_paid=False).exists():
                messages.error(request, 'شما صورت حساب پرداخت نشده دارید')
                return redirect('support_detail')
            else:
                tracking_code = str(uuid4())[:12]
                Support.objects.create(user=user, price=support_plan.price, plan=support_plan,
                                       tracking_code=tracking_code, )
                messages.success(request, 'صورت حساب با موفقیت ایجاد شد')
                return redirect('support_detail')

        else:
            return redirect('login')


class SupportDetail(View):
    def get(self, request):
        if request.user.is_authenticated:
            if Support.objects.filter(user=request.user, is_paid=False).exists():
                support = Support.objects.get(user=request.user, is_paid=False)
                company_info = CompanyInfo.objects.first()
                if support.is_discount_applied:
                    if Discount.objects.filter(code=support.applied_discount_code).exists():
                        discount = Discount.objects.get(code=support.applied_discount_code)
                        if discount.is_expired:
                            set_service_status(support, support.plan.price)
                            messages.error(request, 'کد تخفیف منقضی شده است')
                            return redirect('support_detail')
                        else:
                            discount_price = (support.plan.price * discount.percentage) / 100
                    else:
                        set_service_status(support, support.plan.price)
                        messages.error(request, 'کد تخفیف منسوخ شده است')
                        return redirect('support_detail')
                else:
                    discount_price = 0
                return render(request, 'order_app/support_detail.html',
                              {"order": support, "info": company_info, "price": support.plan.price,
                               "discount_price": int(discount_price)})
            else:
                messages.error(request, 'شما صورت حسابی ندارید')
                return redirect('support')
        else:
            return redirect('login')


class RemoveSupportOrder(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            order = get_object_or_404(Support, tracking_code=pk)
            if request.user == order.user:
                order.delete()
                messages.success(request, 'صورت حساب شما حذف شد')
                return redirect('support')
            else:
                messages.error(request, 'درصورت تکرار اکانت شما مسدود خواهد شد')
        else:
            return redirect('login')


class SupportOrderAddNote(View):
    def post(self, request):
        if request.user.is_authenticated:
            note = request.POST.get('note')
            if Support.objects.filter(user=request.user).exists():
                orders = Support.objects.filter(user=request.user).all()
                for order in orders:
                    if order.is_paid == False:
                        if note:
                            order.note = note
                            order.save()
                            messages.success(request, 'یادداشت شما به صورتحساب اضافه شد')
                            return redirect('support_detail')
                        else:
                            messages.error(request, 'یادداشت خود را به درستی وارد کنید')
                            return redirect('support_detail')
                return redirect('price_list')
            else:
                return redirect('dashboard')
        else:
            redirect('login')


class SupportOrderDetailPrint(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            order = get_object_or_404(Support, tracking_code=pk)
            company_info = CompanyInfo.objects.first()
            if order.is_discount_applied:
                if Discount.objects.filter(code=order.applied_discount_code).exists():
                    discount = Discount.objects.get(code=order.applied_discount_code)
                    if discount.is_expired:
                        set_service_status(order, order.plan.price)
                        messages.error(request, 'کد تخفیف منقضی شده است')
                        return redirect('order_detail')
                    else:
                        discount_price = (order.plan.price * discount.percentage) / 100
                else:
                    set_service_status(order, order.plan.price)
                    messages.error(request, 'کد تخفیف منسوخ شده است')
                    return redirect('order_detail')
            else:
                discount_price = 0
            return render(request, 'order_app/support_order_detail_print.html',
                          {"order": order, "info": company_info, "price": order.plan,
                           "discount_price": int(discount_price)})
        else:
            return redirect('login')


class SupportApplyDiscount(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            code = request.POST.get('code')
            for order in Support.objects.filter(user=user).all():
                if order.is_paid == False:
                    if order.is_discount_applied:
                        messages.error(request, 'کد تخفیف اعمال شده است')
                        return redirect('support_detail')
                    if Discount.objects.filter(code=code).exists():
                        discount = Discount.objects.get(code=code)
                        if not discount.is_expired:
                            discounted_price = calculate_discount_price(discount.percentage, order.price)
                            order.price = discounted_price
                            order.applied_discount_code = code
                            order.is_discount_applied = True
                            order.save()
                            messages.success(request, 'کد تخفیف اعمال شد')
                            return redirect('support_detail')
                        else:
                            messages.error(request, 'کد تخفیف منقضی شده است')
                            return redirect('support_detail')
                    else:
                        messages.error(request, 'کد تخفیف یافت نشد')
                        return redirect('support_detail')
            return redirect('price_list')
        else:
            return redirect('login')


class ExtendSupportOrder(View):
    def get(self, request, pk):
        support_order = get_object_or_404(Support, tracking_code=pk)
        if support_order.is_paid:
            now = jdatetime.datetime.now()
            different_time = support_order.expiration_date - now
            company_info = CompanyInfo.objects.first()
            plans = ExtendSupportPlan.objects.all()
            if different_time.days > 0 and different_time.days < 4:
                return render(request, 'order_app/support_detail.html',
                              {"order": support_order, "info": company_info, "price": support_order.plan.price,
                               'plans': plans})
            elif different_time.days < 0 and different_time.days > -5:
                return render(request, 'order_app/support_detail.html',
                              {"order": support_order, "info": company_info, "price": support_order.plan.price,
                               'plans': plans})
            elif different_time.days == 0:
                return render(request, 'order_app/support_detail.html',
                              {"order": support_order, "info": company_info, "price": support_order.plan.price,
                               'plans': plans})
            else:
                messages.error(request, 'شما تنها 7 روز مانده به اتمام پلن قادر به تمدید هستید')
                return redirect('dashboard')
        else:
            messages.error(request, 'ابتدا صورت حساب خود را پرداخت کنید')
            return redirect('support_detail')
