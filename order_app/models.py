from django.db import models
from django_jalali.db import models as jmodels
from account_app.models import User
from price_app.models import Price, Ability


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveIntegerField(default=0)
    plan_category = models.CharField(max_length=100, default='فروشگاهی')
    plan_type = models.CharField(max_length=100, default='نقره ای')
    applied_discount_code = models.CharField(max_length=20, null=True, blank=True, )
    is_discount_applied = models.BooleanField(default=False, verbose_name='کد تخفیف اعمال شده')
    note = models.TextField(null=True, blank=True)
    tracking_code = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    preparation_percentage = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=False, verbose_name="کامل شده")
    pay_at = jmodels.jDateTimeField(null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'سفارشات'
        verbose_name_plural = 'سفارش'

    def __str__(self):
        return f"{str(self.user.phone)} {self.plan_type} {self.plan_category}"


class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    percentage = models.PositiveIntegerField()
    is_expired = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'کد تخفیف ها'
        verbose_name_plural = 'کد تخفیف'

    def __str__(self):
        return self.code


class SupportPlan(models.Model):
    period = models.CharField(max_length=30)
    ability = models.ManyToManyField(Ability)
    price = models.IntegerField()

    def __str__(self):
        return self.period


class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supports')
    plan = models.ForeignKey(SupportPlan, on_delete=models.CASCADE, related_name='supports', null=True, blank=True)
    price = models.IntegerField()
    tracking_code = models.CharField(max_length=30)
    site_panel_address = models.CharField(max_length=300, null=True, blank=True)
    site_panel_username = models.CharField(max_length=100, null=True, blank=True)
    site_panel_password = models.CharField(max_length=100, null=True, blank=True)
    applied_discount_code = models.CharField(max_length=20, null=True, blank=True, )
    note = models.TextField(null=True, blank=True)
    is_discount_applied = models.BooleanField(default=False, verbose_name='کد تخفیف اعمال شده')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    is_expiration = models.BooleanField(default=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    pay_at = jmodels.jDateTimeField(null=True, blank=True)
    expiration_date = jmodels.jDateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.phone)


class ExtendSupportPlan(models.Model):
    period = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.period
