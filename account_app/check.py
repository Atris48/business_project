import time
from datetime import timedelta
from functools import wraps
from random import randint
from uuid import uuid4
import jdatetime
from account_app.models import Ban, User, Otp



def check_user_ban(phone):
    if Ban.objects.filter(user__phone=phone).exists():
        return True
    return False


def check_user_exist(phone):
    if User.objects.filter(phone=phone).exists():
        return True
    return False


def check_password_valid(password):
    if len(password) < 8 or password.isnumeric() or password.islower() or password.isupper() or password.isalpha():
        return True
    return False


def check_otp_expiration(otp):
    expire_time = otp.expiration_date + timedelta(minutes=2)
    if jdatetime.datetime.now() >= expire_time:
        otp.delete()
        return True
    return False


def create_user(phone, fullname, email, password):
    user = User.objects.create(phone=phone, fullname=fullname, email=email, )
    user.set_password(password)
    user.save()


def create_otp(phone):
    token = str(uuid4())
    random_code = randint(100000, 999999)
    print('random: ', random_code)
    Otp.objects.create(phone=phone, code=random_code, token=token)
    return token

def delete_otp(otp):
    for item in otp:
        item.delete()
