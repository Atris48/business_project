from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from account_app.forms import EditUserProfile
from account_app.models import User, Ban, UserLoginInfo, Otp
from order_app.models import Order, Discount, Support
from ticket_app.models import Chat
from .models import Notification, Announcement
from account_app.check import check_password_valid, delete_otp, create_otp
from .rate_limit import *


def dashboard(request):
    if request.user.is_authenticated:
        all_paid_order = Order.objects.filter(is_paid=True).order_by('-created_at')
        all_paid_support = Support.objects.filter(is_paid=True).order_by('-created_at')
        orders_price = 0
        supports_price = 0
        for item in all_paid_order.all():
            orders_price += item.total_price
        for item in all_paid_support.all():
            supports_price += item.price
        chats = Chat.objects.filter(is_replied=False)
        announcements = Announcement.objects.order_by('-created_at')
        return render(request, 'dashboard_app/dashboard.html',
                      {'all_paid_order': all_paid_order, 'all_paid_support': all_paid_support,
                       'orders_price': orders_price, 'supports_price': supports_price, 'chats': chats,
                       'announcements': announcements})
    else:
        return redirect('login')


def profile(request, phone):
    user = get_object_or_404(User, phone=phone)
    return render(request, 'dashboard_app/profile/profile.html', {'user': user})


def user_edit_profile(request, phone):
    user = get_object_or_404(User, phone=phone)
    if request.user.phone != phone:
        return redirect('index')
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print(form.cleaned_data.get('image'))
            form.save()
            messages.success(request, 'پروفایل شما ویرایش شد')
            return redirect('profile', phone)
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('edit_profile', phone)
    form = EditUserProfile(instance=user)
    return render(request, 'dashboard_app/profile/edit_profile.html', {'form': form, 'user': user})


def remove_notification(request, pk):
    if request.user.is_authenticated:
        notification = get_object_or_404(Notification, id=pk)
        notification.remove.add(request.user)
        return redirect('dashboard')
    else:
        return redirect('index')


def remove_all_remove_notification(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(Q(user=request.user) | Q(user=None))
        for notification in notifications:
            if request.user not in notification.remove.all():
                notification.remove.add(request.user)
        return redirect('dashboard')
    else:
        return redirect('index')


def filter_user(request):
    if request.user.is_staff:
        filter = request.POST.get('filter')
        if filter == 'ban':
            users = Ban.objects.order_by('-id')
        elif filter == 'active':
            users = User.objects.filter(is_active=True).order_by('-created_at')
        elif filter == 'plan':
            users = User.objects.filter(is_buy=True).order_by('-created_at')
        else:
            users = User.objects.order_by('-created_at')
        ban_users = Ban.objects.all()
        all_user = User.objects.all()
        return render(request, 'dashboard_app/user/user_list.html',
                      {'users': users, 'ban_users': ban_users, 'all_user': all_user})

    else:
        return redirect('index')


def user_order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('is_paid')
        paginate = Paginator(orders, 100)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        paid_orders = orders.filter(is_paid=True).count()
        finished_orders = orders.filter(is_finished=True).count()
        not_finished_orders = orders.filter(is_finished=False).count()
        return render(request, 'dashboard_app/order/order_list.html',
                      {"page_obj": page_obj, "count": orders.count(), "is_paid_count": paid_orders,
                       "is_finished_count": finished_orders, "not_finished_orders": not_finished_orders})
    else:
        return redirect('index')


def user_discount_list(request):
    if request.user.is_authenticated:
        discounts = Discount.objects.order_by('-id')
        paginate = Paginator(discounts, 100)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        expired_discount_count = discounts.filter(is_expired=True).count()
        return render(request, 'dashboard_app/discount/discount_list.html',
                      {'page_obj': page_obj, 'discounts': discounts, 'expired_discount_count': expired_discount_count})
    else:
        return redirect('index')


def user_security(request, phone):
    if request.user.is_authenticated:
        user = get_object_or_404(User, phone=phone)
        if request.user.phone != phone:
            return redirect('dashboard')
        user_login_info = UserLoginInfo.objects.filter(user=request.user).order_by('-id')
        return render(request, 'dashboard_app/profile/user_security.html',
                      {'user_login_info': user_login_info, 'user': user})
    else:
        return redirect('login')


@rate_limit_(1, 300, message='امکان تغییر رمز عبور نمیباشد')
def user_change_password(request, phone):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.phone == phone:
                user = get_object_or_404(User, phone=phone)
                old_password = request.POST.get('old_password')
                if user.check_password(old_password):
                    password = request.POST.get('password')
                    confirm_password = request.POST.get('confirm_password')
                    if password != confirm_password:
                        messages.error(request, 'رمز عبور و تکرار رمز عبور یکسان نمیباشد')
                        return redirect('user_security', phone)
                    if check_password_valid(password):
                        messages.error(request, 'رمز عبور باید شامل حداقل 8 کاراکتر،یک حروف بزرگ و کوچک و اعداد باشد')
                        return redirect('user_security', phone)
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'رمز عبور شما تغییر کرد')
                    return redirect('login')
                else:
                    messages.error(request, 'رمز عبور قبلی خود را به درستی وارد کنید')
                    return redirect('user_security', phone)
            else:
                return redirect('dashboard')
    else:
        return redirect('login')


@rate_limit_(1, 120, message='امکان فعال سازی ورود دو مرحله ای نمیباشد')
def active_two_step_login(request, phone):
    if request.user.is_authenticated:
        user = get_object_or_404(User, phone=phone)
        print(user.is_two_step)
        if user.is_two_step:
            messages.error(request, 'ورود دو مرحله ای اکانت شما فعال است')
            return redirect('dashboard')
        if request.user == user:
            if Otp.objects.filter(phone=user.phone).exists():
                opt = Otp.objects.filter(phone=user.phone).all()
                delete_otp(opt)
                token = create_otp(user.phone)
                messages.success(request, 'کد اعتبار سنجی به شماره شما ارسال شد')
                return redirect(reverse('check_two_step_otp') + f'?token={token}')
            else:
                token = create_otp(user.phone)
                messages.success(request, 'کد اعتبار سنجی به شماره شما ارسال شد')
                return redirect(reverse('check_two_step_otp') + f'?token={token}')
        else:
            return redirect('dashboard')
    else:
        return redirect('login')


@rate_limit_(1, 120, message='امکان فعال سازی ورود دو مرحله ای نمیباشد')
def check_two_step_otp(request):
    if request.user.is_authenticated:
        phone = request.user.phone
        user = get_object_or_404(User, phone=phone)
        if request.method == 'POST':
            code1 = request.POST.get('code1')
            code2 = request.POST.get('code2')
            code3 = request.POST.get('code3')
            code4 = request.POST.get('code4')
            code5 = request.POST.get('code5')
            code6 = request.POST.get('code6')
            code = int(f'{code1}{code2}{code3}{code4}{code5}{code6}')
            token = request.POST.get('token')
            if Otp.objects.filter(token=token, code=code, phone=user.phone).exists():
                user.is_two_step = True
                user.save()
                Otp.objects.filter(token=token, code=code, phone=user.phone).delete()
                messages.success(request, 'ورود دو مرحله ای اکانت شما فعال شد')
                return redirect('dashboard')
            else:
                messages.error(request, 'کد اعتبار سنجی صحیح نمیباشد')
                return redirect(reverse('check_two_step_otp') + f'?token={token}')
        return render(request, 'dashboard_app/user/two_step_active_check_otp.html')
    else:
        return redirect('login')


@rate_limit_(1, 120, message='امکان غیرفعال سازی ورود دو مرحله ای نمیباشد')
def inactive_two_step_login(request, phone):
    if request.user.is_authenticated:
        user = get_object_or_404(User, phone=phone)
        if not user.is_two_step:
            messages.error(request, 'ورود دو مرحله ای اکانت شما غیر فعال است')
            return redirect('dashboard')
        if request.user == user:
            if Otp.objects.filter(phone=user.phone).exists():
                opt = Otp.objects.filter(phone=user.phone).all()
                delete_otp(opt)
                token = create_otp(user.phone)
                messages.success(request, 'کد اعتبار سنجی به شماره شما ارسال شد')
                return redirect(reverse('check_two_step_otp') + f'?token={token}')
            else:
                token = create_otp(user.phone)
                messages.success(request, 'کد اعتبار سنجی به شماره شما ارسال شد')
                return redirect(reverse('check_two_step_otp') + f'?token={token}')
        else:
            return redirect('dashboard')
    else:
        return redirect('login')


@rate_limit_(1, 120, message='امکان فعال سازی ورود دو مرحله ای نمیباشد')
def check_inactive_otp(request):
    if request.user.is_authenticated:
        phone = request.user.phone
        user = get_object_or_404(User, phone=phone)
        if request.method == 'POST':
            code1 = request.POST.get('code1')
            code2 = request.POST.get('code2')
            code3 = request.POST.get('code3')
            code4 = request.POST.get('code4')
            code5 = request.POST.get('code5')
            code6 = request.POST.get('code6')
            code = int(f'{code1}{code2}{code3}{code4}{code5}{code6}')
            token = request.POST.get('token')
            if Otp.objects.filter(token=token, code=code, phone=user.phone).exists():
                user.is_two_step = False
                user.save()
                Otp.objects.filter(token=token, code=code, phone=user.phone).delete()
                messages.success(request, 'ورود دو مرحله ای اکانت شما غیر فعال شد')
                return redirect('dashboard')
            else:
                messages.error(request, 'کد اعتبار سنجی صحیح نمیباشد')
                return redirect(reverse('check_two_step_otp') + f'?token={token}')
        return render(request, 'dashboard_app/user/two_step_active_check_otp.html')
    else:
        return redirect('login')


def user_support_order_list(request):
    if request.user.is_authenticated:
        orders = Support.objects.filter(user=request.user).order_by('is_paid')
        paginate = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
        paid_orders = orders.filter(is_paid=True).count()
        expiration_orders = orders.filter(is_expiration=True).count()
        not_expiration_orders = orders.filter(is_expiration=False).count()
        return render(request, 'dashboard_app/support/support_order_list.html',
                      {"page_obj": page_obj, "count": orders.count(), "is_paid_count": paid_orders,
                       "is_finished_count": expiration_orders, "not_finished_orders": not_expiration_orders})
    else:
        return redirect('index')
