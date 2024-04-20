from django.urls import path
from . import views

urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('check-otp', views.CheckOtpView.as_view(), name='check_otp'),
    path('resend-active-code', views.ResendActiveCodeView.as_view(), name='resend_active_code'),
    path('resubmit-otp', views.ResubmitOtpCodeView.as_view(), name='resubmit_otp'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget_password'),
    path('forget-password-check-otp', views.ForgetPasswordCheckOtpView.as_view(), name='forget_password_check_otp'),
    path('change-password/<str:phone>', views.ChangePassword.as_view(), name='change_password'),
    path('check-two-step-login-otp', views.CheckTwoStepLoginOtp.as_view(), name='check_two_step_login_otp'),
]
