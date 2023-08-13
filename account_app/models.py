from django.urls import reverse
from django_jalali.db import models as jmodels
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from jdatetime import *


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=phone,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,

        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    SEX = (
        ('مرد', 'مرد'),
        ('زن', 'زن'),
    )
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,

    )
    fullname = models.CharField(max_length=80, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=11, unique=True, verbose_name="تلفن همراه")
    image = models.ImageField(upload_to='user/images', null=True, blank=True, verbose_name='عکس پروفایل')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    sex = models.CharField(choices=SEX, null=True, blank=True, max_length=20, verbose_name='جنسیت')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان عضویت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")
    birthday = models.CharField(max_length=20, null=True, blank=True, verbose_name='تاریخ تولد')
    is_active = models.BooleanField(default=False, verbose_name="وضعیت کاربر")
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Ban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user.phone)


class Otp(models.Model):
    token = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه')
    code = models.SmallIntegerField(verbose_name='کد اعتبار سنجی')
    fullname = models.CharField(max_length=80, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,

    )
    password1 = models.CharField(max_length=50, verbose_name="گذرواژه")
    password2 = models.CharField(max_length=50, verbose_name="تکرار گذرواژه")
    expiration_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ انقضا')

    class Meta:
        verbose_name = 'اعتبار سنجی'
        verbose_name_plural = 'اعتبار سنجی ها'

    def __str__(self):
        return self.phone
