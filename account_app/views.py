from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from account_app.forms import LoginForm, RegisterForm
from .check import *
from .rate_limit import *


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, 'account_app/login.html', {'form': form})

    @method_decorator(rate_limit_login(3, 180, 'امکان وارد شدن وجود ندارد'))
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if check_user_ban(cd['phone']):
                messages.error(request, 'حساب شما مسدود شده است')
                return redirect('login')
            if check_user_exist(cd['phone']):
                user = User.objects.get(phone=cd['phone'])
                if user.is_active == False:
                    messages.error(request, 'اکانت خود را فعال کنید')
                    return redirect('resend_active_code')
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "خوش آمدید")
                return redirect('dashboard')
            else:
                form.add_error("password", "رمز عبور وارد شده صحیح نیست")
                form.add_error("phone", "تلفن همراه وارد شده صحیح نیست")
                messages.error(request, 'اطلاعات وارد شده صحیح نیست')
                return redirect('login')
        else:
            messages.error(request, "اطلاعات وارد شده صحیح نیست")
            return redirect('login')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


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
                # SMS.verification({'receptor': phone, 'type': '1', 'template': 'verifyotp', 'param1': random_code})
                # token = get_random_string(length=100, allowed_chars='Ahh22') یا پایین
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
                        # SMS.verification(
                        #     {'receptor': phone, 'type': '1', 'template': 'forgetpass', 'param1': random_code})
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
                messages.error(request, 'کاربر یافت نشد')
                return redirect('change_password')
        else:
            if request.user.phone == phone:
                user = get_object_or_404(User, phone=phone)
                old_password = request.POST.get('old_password')
                if user.check_password(old_password):
                    password = request.POST.get('password')
                    confirm_password = request.POST.get('confirm_password')
                    if password != confirm_password:
                        messages.error(request, 'رمز عبور و تکرار رمز عبور یکسان نمیباشد')
                        return redirect('change_password', phone)
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'رمز عبور شما تغییر کرد')
                    return redirect('login')
                else:
                    messages.error(request, 'رمز عبور قبلی خود را به درستی وارد کنید')
                    return redirect('change_password', phone)
            else:
                messages.error(request, 'رمز عبور و تکرار رمز عبور یکسان نمیباشد')
                return redirect('change_password', phone)
