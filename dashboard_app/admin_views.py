from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from account_app.forms import AdminCreateUserForm, EditAdminProfile
from account_app.models import User, Ban
from checklist_app.models import Checklist
from dashboard_app.forms import EditOrderForm, CreateNotificationForm, EditSupportOrderForm, OrderPrice, \
    SupportPriceForm, ExtendSupportPlanForm, CreateAnnouncementForm
from order_app.models import Discount, Order, Support, SupportPlan, ExtendSupportPlan
from uuid import uuid4

from price_app.models import Price, PriceCategory
from sms.sms import send_sms


def admin_order_list(request):
    if request.user.is_staff:
        orders = Order.objects.order_by('-created_at')
        paginate = Paginator(orders, 100)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        paid_orders = orders.filter(is_paid=True).count()
        finished_orders = orders.filter(is_finished=True).count()
        not_paid_orders = orders.filter(is_paid=False).count()
        return render(request, 'dashboard_app/order/order_list.html',
                      {"page_obj": page_obj, "count": orders.count(), 'paid_order': paid_orders,
                       'finished_order': finished_orders, 'not_paid_orders': not_paid_orders})
    else:
        return redirect('index')


def admin_remove_order(reqeust, pk):
    if reqeust.user.is_staff:
        order = get_object_or_404(Order, tracking_code=pk)
        order.delete()
        messages.success(reqeust, 'سفارش حذف شد')
        return redirect('admin_order_list')
    else:
        return redirect('index')


def admin_add_order(request):
    if request.user.is_staff:
        users = User.objects.all()
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            if Order.objects.filter(user_id=user_id, is_paid=False):
                messages.error(request, 'کاربر مورد ننظر صورت حساب پرداخت نشده دارد')
                return redirect('admin_order_list')
            total_price = request.POST.get('total_price')
            plan_category = request.POST.get('plan_category')
            plan_type = request.POST.get('plan_type')
            unique_code = uuid4()
            tracking_code = str(unique_code)[:12]
            order = Order.objects.create(user_id=user_id, total_price=total_price, plan_category=plan_category,
                                         plan_type=plan_type, tracking_code=tracking_code)
            Checklist.objects.create(order=order)
            messages.success(request, 'صورت حساب با موفقیت ایجاد شد')
            return redirect('admin_order_list')
        plan_categories = PriceCategory.objects.all()
        return render(request, 'dashboard_app/order/add_order.html',
                      {"users": users, "plans": plan_categories})
    else:
        return redirect('index')


def admin_edit_order(request, pk):
    if request.user.is_staff:
        order = get_object_or_404(Order, tracking_code=pk)
        if request.method == 'POST':
            form = EditOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, 'سفارش ویرایش شد')
                return redirect('edit_order', pk)
            else:
                messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
                return redirect('edit_order', pk)
        form = EditOrderForm(instance=order)
        users = User.objects.all()
        user = order.user
        return render(request, 'dashboard_app/order/edit_order.html', {'form': form, 'users': users, 'user': user})
    else:
        return redirect('index')


def admin_support_order_list(request):
    if request.user.is_staff:
        orders = Support.objects.order_by('-created_at')
        paginate = Paginator(orders, 100)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        paid_orders = orders.filter(is_paid=True).count()
        expiration_orders = orders.filter(is_expiration=True).count()
        not_paid_orders = orders.filter(is_paid=False).count()
        return render(request, 'dashboard_app/support/support_order_list.html',
                      {"page_obj": page_obj, "count": orders.count(), 'paid_order': paid_orders,
                       'finished_order': expiration_orders, 'not_paid_orders': not_paid_orders})
    else:
        return redirect('index')


def admin_edit_support_order(request, pk):
    if request.user.is_staff:
        order = get_object_or_404(Support, tracking_code=pk)
        if request.method == 'POST':
            form = EditSupportOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, 'سفارش ویرایش شد')
                return redirect('admin_edit_support_order', pk)
            else:
                messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
                return redirect('admin_edit_support_order', pk)
        form = EditSupportOrderForm(instance=order)
        users = User.objects.all()
        return render(request, 'dashboard_app/support/edit_support_order.html', {'form': form, 'users': users})
    else:
        return redirect('index')


def admin_add_support_order(request):
    if request.user.is_staff:
        users = User.objects.all()
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            if Support.objects.filter(user_id=user_id, is_paid=False):
                messages.error(request, 'کاربر مورد ننظر صورت حساب پرداخت نشده دارد')
                return redirect('admin_support_order_list')
            total_price = request.POST.get('total_price')
            plan_id = request.POST.get('plan_category')
            expiration_date = request.POST.get('expiration')
            plan = SupportPlan.objects.get(id=plan_id)
            unique_code = uuid4()
            tracking_code = str(unique_code)[:12]
            Support.objects.create(user_id=user_id, price=total_price, plan=plan,
                                   tracking_code=tracking_code, expiration_date=expiration_date)
            messages.success(request, 'صورت حساب با موفقیت ایجاد شد')
            return redirect('admin_support_order_list')
        plans = SupportPlan.objects.all()
        return render(request, 'dashboard_app/support/add_support_order.html',
                      {"users": users, "plans": plans})
    else:
        return redirect('index')


def admin_discount_list(request):
    if request.user.is_staff:
        discounts = Discount.objects.order_by('-id')
        paginate = Paginator(discounts, 100)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        expired_discount_count = discounts.filter(is_expired=True).count()
        return render(request, 'dashboard_app/discount/discount_list.html',
                      {'discounts': discounts, 'page_obj': page_obj, 'expired_discount_count': expired_discount_count})
    else:
        return redirect('index')


def admin_remove_discount(request, pk):
    if request.user.is_staff:
        discount = get_object_or_404(Discount, id=pk)
        discount.delete()
        messages.success(request, 'کد تخفیف حذف شد')
        return redirect('admin_discount_list')
    else:
        return redirect('index')


def admin_expire_discount(request, pk):
    if request.user.is_staff:
        discount = get_object_or_404(Discount, id=pk)
        if discount.is_expired:
            discount.is_expired = False
            discount.save()
            messages.success(request, 'کد تخفیف فعال شد')
            return redirect('admin_discount_list')
        else:
            discount.is_expired = True
            discount.save()
            messages.success(request, 'کد تخفیف منقضی شد')
            return redirect('admin_discount_list')
    else:
        return redirect('index')


def admin_add_discount(request):
    if request.user.is_staff:
        if request.method == 'POST':
            code = request.POST.get('code')
            percentage = request.POST.get('percentage')
            if Discount.objects.filter(code=code, percentage=percentage):
                return redirect('admin_add_discount')
            Discount.objects.create(code=code, percentage=percentage)
            messages.success(request, 'کد تخفیف ایجاد شد')
            return redirect('admin_discount_list')
        return render(request, 'dashboard_app/discount/add_discount.html')
    else:
        return redirect('index')


def admin_edit_profile(request, phone):
    user = get_object_or_404(User, phone=phone)
    if request.method == 'POST':
        form = EditAdminProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل شما ویرایش شد')
            return redirect('admin_edit_profile', phone)
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('edit_profile', phone)
    form = EditAdminProfile(instance=user)
    return render(request, 'dashboard_app/profile/edit_profile.html', {'form': form, 'user': user})


def admin_remove_user(request, phone):
    if request.user.is_staff:
        user = get_object_or_404(User, phone=phone)
        user.delete()
        return redirect('all_user_list')
    else:
        return redirect('index')


def admin_ban_user(request, phone):
    if request.user.is_staff:
        user = get_object_or_404(User, phone=phone)
        if Ban.objects.filter(user=user).exists():
            Ban.objects.get(user=user).delete()
            send_sms(user.phone, 'unbanuser', parm1=user.fullname)
            messages.success(request, 'کاربر از مسدودیت خارج شد')
            return redirect('all_user_list')
        else:
            Ban.objects.create(user=user)
            send_sms(user.phone, 'banuser', parm1=user.fullname)
            messages.success(request, 'کاربر مسدود شد')
            return redirect('all_user_list')
    else:
        return redirect('index')


def admin_create_user(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AdminCreateUserForm(request.POST)
            if form.is_valid():
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                if password != confirm_password:
                    messages.error(request, 'رمز عبور و تایید رمز عبور یکسان نمیباشد')
                    return redirect('admin_create_user')
                elif not password or not confirm_password:
                    messages.error(request, 'رمز عبور اجباری است')
                    return redirect('admin_create_user')
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                messages.success(request, 'کاربر با موفقیت ساخته شد')
                return redirect('all_user_list')
            else:
                messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
                return redirect('all_user_list')
        form = AdminCreateUserForm()
        return render(request, 'dashboard_app/profile/edit_profile.html', {'form': form})
    else:
        return redirect('index')


def admin_change_password(request, phone):
    if request.user.is_staff:
        user = get_object_or_404(User, phone=phone)
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                messages.error(request, 'رمز عبور و تکرار رمز عبور یکسان نمیباشد')
                return redirect('admin_change_password', phone)
            user.set_password(password)
            user.save()
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
            return redirect('all_user_list')
        return render(request, 'dashboard_app/profile/admin_change_password.html', {'user': user})
    else:
        return redirect('index')


def all_user_list(request):
    if request.user.is_staff:
        users = User.objects.order_by('-created_at')
        paginate = Paginator(users, 100)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        ban_users = Ban.objects.all()
        all_user = User.objects.all()
        return render(request, 'dashboard_app/user/user_list.html',
                      {'page_obj': page_obj, 'ban_users': ban_users, 'all_user': all_user})
    else:
        return redirect('index')


def admin_create_notification(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CreateNotificationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "نوتیفیکیشن ایجاد شد")
                return redirect('dashboard')
        form = CreateNotificationForm()
        users = User.objects.all()
        return render(request, 'dashboard_app/notification/create_notification.html', {'form': form, 'users': users})
    else:
        return redirect('index')


def admin_create_announcement(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CreateAnnouncementForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "اعلان ایجاد شد")
                return redirect('dashboard')
        form = CreateAnnouncementForm()
        users = User.objects.all()
        return render(request, 'dashboard_app/notification/create_notification.html', {'form': form, 'users': users})
    else:
        return redirect('index')


def plans_price_list(request):
    if request.user.is_staff:
        order_prices = Price.objects.all()
        support_prices = SupportPlan.objects.all()
        extend_support_prices = ExtendSupportPlan.objects.all()
        return render(request, 'dashboard_app/price_list.html',
                      {'order_prices': order_prices, 'support_prices': support_prices,
                       'extend_support_prices': extend_support_prices})
    else:
        return redirect('index')


def change_website_order_price(request, pk):
    if request.user.is_staff:
        price = get_object_or_404(Price, id=pk)
        if request.method == 'POST':
            form = OrderPrice(request.POST, instance=price)
            if form.is_valid():
                form.save()
                messages.success(request, 'قیمت با موفقیت تغییر کرد')
                return redirect('dashboard')
            else:
                messages.success(request, 'اطلاعات وارد شده صحیح نمیباشد')
                return redirect('dashboard')
        form = OrderPrice(instance=price)
        return render(request, 'dashboard_app/price.html', {'form': form})
    else:
        return redirect('index')


def change_support_plan_price(request, pk):
    if request.user.is_staff:
        price = get_object_or_404(SupportPlan, id=pk)
        if request.method == 'POST':
            form = SupportPriceForm(request.POST, instance=price)
            if form.is_valid():
                form.save()
                messages.success(request, 'قیمت با موفقیت تغییر کرد')
                return redirect('dashboard')
            else:
                messages.success(request, 'اطلاعات وارد شده صحیح نمیباشد')
                return redirect('dashboard')
        form = SupportPriceForm(instance=price)
        return render(request, 'dashboard_app/price.html', {'form': form})
    else:
        return redirect('index')


def change_extend_plan_price(request, pk):
    if request.user.is_staff:
        price = get_object_or_404(ExtendSupportPlan, id=pk)
        if request.method == 'POST':
            form = ExtendSupportPlanForm(request.POST, instance=price)
            if form.is_valid():
                form.save()
                messages.success(request, 'قیمت با موفقیت تغییر کرد')
                return redirect('dashboard')
            else:
                messages.success(request, 'اطلاعات وارد شده صحیح نمیباشد')
                return redirect('dashboard')
        form = ExtendSupportPlanForm(instance=price)
        return render(request, 'dashboard_app/price.html', {'form': form})
    else:
        return redirect('index')
