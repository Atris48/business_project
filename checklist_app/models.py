from django.db import models
from django_jalali.db import models as jmodels

from order_app.models import Order


class Checklist(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    template = models.BooleanField(default=False, verbose_name="آماده سازی قالب سایت")
    account_system = models.BooleanField(default=False, verbose_name="ایجاد بخش حساب کاربری")
    database = models.BooleanField(default=False, verbose_name="ایجاد دیتابیس سایت")
    back_end = models.BooleanField(default=False, verbose_name="نوشتن کد بخش پردازش سایت")
    customize_admin_panel = models.BooleanField(default=False, verbose_name="ایجاد و شخصی سازی پنل ادمین")
    test = models.BooleanField(default=False, verbose_name="تست عملکرد وبسایت")
    deploy = models.BooleanField(default=False, verbose_name="انتقال پروژه به هاست")
    finished = models.BooleanField(default=False, verbose_name="تحویل وبسایت به شما")
    created_at = jmodels.jDateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = jmodels.jDateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.order.user.phone)
