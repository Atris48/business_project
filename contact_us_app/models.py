from django.db import models
from django_jalali.db import models as jmodels


class ContactUs(models.Model):
    fullname = models.CharField(max_length=50, verbose_name='نام')
    phone = models.IntegerField(default=0, verbose_name='شماره تلفن')
    email = models.EmailField(verbose_name='ایمیل')
    message = models.TextField(verbose_name='پیام')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=11)
    phone_2 = models.CharField(max_length=11, null=True, blank=True)
    phone_3 = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField()
    email_2 = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.phone
