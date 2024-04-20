from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from account_app.forms import LoginForm, RegisterForm
from dashboard_app.models import Notification
from order_app.models import Support
from .check import *
from .models import UserLoginInfo, UserLoginCount
from .rate_limit import *
from sms.sms import send_sms


def check_support_plan():
    supoorts = Support.objects.filter(is_paid=True).all()
    for item in supoorts:
        now = jdatetime.datetime.now()
        if item.expiration_date:
            different_time = item.expiration_date - now

            if different_time.days > 0 and different_time.days < 4:
                if different_time.days == 3:
                    Notification.objects.create(user=item.user, title='تمدید اشتراک',
                                                description=f'کاربر محترم اشتراک شما در حال اتمام است، برای تمدید کلیک کنید',
                                                url=reverse('extend_support_order',
                                                            kwargs={'pk': item.tracking_code}))
                    send_sms(item.user.phone, 'extendsoppurt1', parm1=item.user.fullname)
            elif different_time.days < 0 and different_time.days > -5:
                if different_time.days == -2:
                    Notification.objects.create(user=item.user, title='تمدید اشتراک',
                                                description=f'کاربر محترم اشتراک شما منقضی شده است، برای تمدید کلیک کنید',
                                                url=reverse('extend_support_order',
                                                            kwargs={'pk': item.tracking_code}))
                    send_sms(item.user.phone, 'extendsoppurt2', parm1=item.user.fullname)
                item.is_expiration = True
                item.save()
            elif different_time.days == 0:
                Notification.objects.create(user=item.user, title='تمدید اشتراک',
                                            description=f'کاربر محترم اشتراک شما منقضی شد، برای تمدید کلیک کنید',
                                            url=reverse('extend_support_order',
                                                        kwargs={'pk': item.tracking_code}))
                item.is_expiration = True
                item.save()
            else:
                pass
        else:
            pass


class CheckTwoStepLoginOtp(View):
    def get(self, request):
        return render(request, 'account_app/two_step_login_check_otp.html')

    def post(self, request):
        code1 = request.POST.get('code1')
        code2 = request.POST.get('code2')
        code3 = request.POST.get('code3')
        code4 = request.POST.get('code4')
        code5 = request.POST.get('code5')
        code6 = request.POST.get('code6')
        code = int(f'{code1}{code2}{code3}{code4}{code5}{code6}')
        token = request.POST.get('token')
        phone = request.session.get('phone')
        user = get_object_or_404(User, phone=phone)
        if Otp.objects.filter(token=token, code=code, phone=phone).exists():
            login(request, user)
            info = request.user_agent
            ip_address = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
            UserLoginInfo.objects.create(user=user, os=info.os.family, browser=info.browser.family,
                                         date=jdatetime.datetime.now(), ip=ip_address)
            messages.success(request, 'خوش آمدید')
            if UserLoginCount.objects.filter(user=user).exists():
                user_login_count = UserLoginCount.objects.get(user=user)
                user_login_count.count += 1
                user_login_count.save()
            else:
                UserLoginCount.objects.create(user=user, count=1)
            Otp.objects.filter(token=token, code=code, phone=phone).delete()
            return redirect('dashboard')
        else:
            messages.error(request, 'کد اعتبار سنجی صحیح نمیباشد')
            return redirect(reverse('check_two_step_otp') + f'?token={token}')


class UserRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm()
        return render(request, 'account_app/register.html', {'form': form})

    @method_decorator(rate_limit_register(2, 180, 'امکان ثبت نام وجود ندارد'))
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm(request.POST)
        if request.POST.get("agree-term") != 'on':
            messages.error(request, 'قوانین سایت را بپذیرید')
            return redirect('register')
        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            phone = form.cleaned_data.get('phone')
            if check_user_ban(phone):
                messages.error(request, 'حساب شما مسدود شده است')
                return redirect('login')
            if check_password_valid(password):
                messages.error(request, 'رمز عبور باید شامل حداقل 8 کاراکتر،یک حروف بزرگ و کوچک و اعداد باشد')
                return redirect('register')
            if check_user_exist(phone):
                user = User.objects.get(phone=phone)
                if user.is_active == False:
                    messages.error(request, 'اکانت شما غیر فعال است.جهت فعالسازی کد اعتبار سنجی را تایید کنید')
                    return redirect('resend_otp')
                else:
                    messages.error(request, 'شما قبلا ثبت نام کرده اید از این قسمت وارد شوید')
                    return redirect('login')
            create_user(phone, fullname, email, password)
            if Otp.objects.filter(phone=phone).exists():
                delete_otp(Otp.objects.filter(phone=phone))
            token = create_otp(phone)
            otp = Otp.objects.get(token=token)
            send_sms(otp.phone, 'verifyotp', parm1=otp.code)
            request.session['phone'] = phone
            messages.success(request, 'کد تایید ارسال شده را وارد کنید')
            return redirect(reverse('check_otp') + f'?token={token}')
        else:
            messages.error(request, "اطلاعات وارد شده صحیح نیست")

        return render(request, 'account_app/register.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'account_app/check_otp.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        token = request.GET.get('token')
        code = request.POST.get('code')
        if Otp.objects.filter(code=code, token=token).exists():
            otp = Otp.objects.get(token=token)
            if check_otp_expiration(otp=otp):
                messages.error(request, 'کد اعتبار سنجی شما منقضی شده است')
                return redirect('check_otp')
            user, is_create = User.objects.get_or_create(phone=otp.phone)
            user.is_active = True
            user.set_password(user.password)
            delete_otp(Otp.objects.filter(phone=user.phone))
            user.save()
            login(request, user)
            messages.success(request, 'خوش آمدید')
            return redirect('dashboard')
        else:
            messages.error(request, 'کد وارد شده اشتباه است', )
            return redirect(reverse('check_otp') + f'?token={token}')


class ResubmitOtpCodeView(View):
    @method_decorator(rate_limit_resubmit_otp(2, 180, 'ارسال مجدد کد اعتبار سنجی امکان پذیر نمیباشد'))
    def get(self, request):
        if request.session.get('phone'):
            phone = request.session.get('phone')
            if Otp.objects.filter(phone=phone).exists():
                delete_otp(Otp.objects.filter(phone=phone))
            # SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'verifyotp', 'param1': random_code})
            token = create_otp(phone)
            otp = Otp.objects.get(token=token)
            send_sms(otp.phone, 'resubmitcode', parm1=otp.code)
            return redirect(reverse('check_otp') + f'?token={token}')
        else:
            messages.error(request, 'شماره خود را دوباره وارد کنید')
            return redirect('resend_otp')


class ResendActiveCodeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'account_app/resend_active_code.html')

    @method_decorator(rate_limit_resend_active_code(2, 120, 'ارسال مجدد کد اعتبار سنجی امکان پذیر نمیباشد'))
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        phone = request.POST.get('phone')
        if check_user_ban(phone):
            messages.error(request, 'حساب شما مسدود شده است')
            return redirect('index')
        if check_user_exist(phone):
            user = User.objects.get(phone=phone)
            if user.is_active == False:
                if Otp.objects.filter(phone=phone).exists():
                    delete_otp(Otp.objects.filter(phone=phone))
                token = create_otp(phone)
                otp = Otp.objects.get(token=token)
                send_sms(otp.phone, 'resubmitcode', parm1=otp.code)
                return redirect(reverse('check_otp') + f'?token={token}')
            else:
                messages.error(request, 'اکانت شما فعال میباشد')
                return redirect('login')
        else:
            messages.error(request, 'اکانت مورد نظر یافت نشد')
            return redirect('register')


# @rate_limit_forget_otp(1, 120, 'امکان ارسال کد اعتبار سنجی نمیباشد')
class ForgetPasswordView(View):
    def get(self, request):
        return render(request, 'account_app/forget_password.html')

    def post(self, request):
        if not request.user.is_authenticated and request.method == 'POST':
            phone = request.POST.get('phone')
            if check_user_ban(phone):
                messages.error(request, 'حساب شما مسدود شده است')
                return redirect('index')
            if check_user_exist(phone):
                user = User.objects.get(phone=phone)
                if user.is_active:
                    if Otp.objects.filter(phone=phone).exists():
                        delete_otp(Otp.objects.filter(phone=phone))
                        token = create_otp(phone)
                        otp = Otp.objects.get(token=token)
                        send_sms(otp.phone, 'forgetpass', parm1=user.fullname, parm2=otp.code)
                        messages.success(request, 'کد تایید ارسال شده را وارد کنید')
                        return redirect(reverse('forget_password_check_otp') + f'?token={token}&phone={phone}')
                    else:
                        token = create_otp(phone)
                        # SMS.verification(
                        #     {'receptor': phone, 'type': '1', 'template': 'forgetpass', 'param1': random_code})
                        messages.success(request, 'کد تایید ارسال شده را وارد کنید')
                        return redirect(reverse('forget_password_check_otp') + f'?token={token}&phone={phone}')
                else:
                    messages.error(request, 'اکانت شما فعال نمیباشد')
                    return redirect('resend_active_code')
            else:
                messages.error(request, 'کاربر یافت نشد')
                return redirect('forget_password')
        else:
            return redirect('index')


class ForgetPasswordCheckOtpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'account_app/forget_password_check_otp.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        token = request.POST.get('token')
        code = request.POST.get('code')
        if Otp.objects.filter(code=code, token=token).exists():
            otp = Otp.objects.get(token=token)
            if check_otp_expiration(otp=otp):
                messages.error(request, 'کد اعتبار سنجی شما منقضی شده است')
                return redirect('forget_password')
            request.session['phone'] = otp.phone
            request.session['token'] = token
            otp.delete()
            messages.success(request, 'رمز جدید خود را وارد کنید')
            return redirect('change_password', otp.phone)
        else:
            messages.error(request, 'کد وارد شده اشتباه است', )
            return redirect(reverse('forget_password_check_otp') + f'?token={token}')


class ChangePassword(View):
    def get(self, request, phone):
        return render(request, 'account_app/change_password.html')

    def post(self, request, phone):
        if not request.user.is_authenticated:
            if check_user_exist(phone):
                if request.session.get('token'):
                    user = User.objects.get(phone=phone)
                    password = request.POST.get('password')
                    confirm_password = request.POST.get('confirm_password')
                    if check_password_valid(password):
                        messages.error(request, 'رمز عبور باید شامل حداقل 8 کاراکتر،یک حروف بزرگ و کوچک و اعداد باشد')
                        return redirect('change_password')
                    if password != confirm_password:
                        messages.error(request, 'رمز عبور و تکرار رمز عبور یکسان نمیباشد')
                        return redirect('change_password')
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
                    return redirect('login')
                else:
                    messages.error(request, 'جهت تغییر رمز عبور شماره تلفن خود را وارد کنید')
                    return redirect('forget_password')
            else:
                messages.error(request, 'کاربر یافت نشد')
                return redirect('change_password')
        else:
            return redirect('dashboard')
