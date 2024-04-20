import jalali_date
from django import template
import jdatetime

register = template.Library()


@register.filter()
def get_days_ago(date):
    now = jdatetime.datetime.now()
    days_ago = now.day - date.day
    return days_ago


@register.filter()
def ad_date_to_solar(ad_date):
    solar = jalali_date.date2jalali(ad_date)
    return solar


@register.filter()
def get_active_users(users):
    return users.filter(is_active=True).order_by('-created_at').count()


@register.filter()
def get_has_plan_users(users):
    return users.filter(is_buy=True).order_by('-created_at').count()


@register.filter()
def get_reverse_date(date):
    replace_date = str(date).split('-')
    shamsi_date = f'{replace_date[2]}-{replace_date[1]}-{replace_date[0]}'
    return shamsi_date


@register.filter()
def get_tax(price):
    tax_price = (price * 9) / 100
    return int(tax_price)


@register.filter()
def get_total_price(price):
    tax_price = (price * 9) / 100
    return int(price + tax_price)


@register.filter()
def get_paid_order_count(orders):
    total = 0
    for order in orders:
        if order.is_paid == True:
            total += 1
    return total


@register.filter()
def get_paid_order_price(orders):
    total = 0
    for order in orders:
        if order.is_paid == True:
            total += order.total_price
    return total


@register.filter()
def get_paid_support_price(orders):
    total = 0
    for order in orders:
        if order.is_paid == True:
            total += order.price
    return total


@register.filter()
def get_paid_support_count(orders):
    total = 0
    for order in orders:
        if order.is_paid == True:
            total += 1
    return total


@register.filter()
def get_slice_order(orders):
    order = orders.filter(is_paid=True).order_by('-created_at')[:3]
    return order


@register.filter()
def get_slice_notification(notifications):
    order = notifications.order_by('-created_at')[:3]
    return order


@register.filter()
def get_slice_supports(supports):
    order = supports.filter(is_paid=True).order_by('-created_at')[:3]
    return order


@register.filter()
def get_not_finished_order_count(orders):
    total = 0
    for order in orders:
        if order.is_finished == False:
            total += 1
    return total


@register.filter()
def get_finished_order_count(orders):
    total = 0
    for order in orders:
        if order.is_finished:
            total += 1
    return total


@register.filter()
def order_paid_percent(orders):
    total = 0
    for order in orders:
        if order.is_paid == True:
            total += 1
    if orders.count() > 0:
        percent = (total / orders.count()) * 100
    else:
        percent = 0
    return percent


@register.filter()
def order_not_finished_percent(orders):
    total = 0
    for order in orders:
        if order.is_finished == False:
            total += 1
    if orders.filter(is_paid=True).count() > 0:
        percent = (total / orders.filter(is_paid=True).count()) * 100
    else:
        percent = 0
    return percent


@register.filter()
def order_finished_percent(orders):
    total = 0
    for order in orders:
        if order.is_finished:
            total += 1
    if orders.filter(is_paid=True).count() > 0:
        percent = (total / orders.filter(is_paid=True).count()) * 100
    else:
        percent = 0
    return percent


@register.filter()
def extend_support_plan(support):
    if support.expiration_date == None:
        return False
    if support.is_paid:
        now = jdatetime.datetime.now()
        different_time = support.expiration_date - now
        if different_time.days > 0 and different_time.days < 4:
            return True
        elif different_time.days < 0 and different_time.days > -5:
            return True
        elif different_time.days == 0:
            return True
        else:
            return False
    else:
        return False


@register.filter()
def time_to_extend_support(support):
    if support.expiration_date == None:
        return 'ناریخ انقضا ندارد'
    if support.is_paid:
        now = jdatetime.datetime.now()
        different_time = support.expiration_date - now
        return f'{different_time.days} روز مانده تا تمدید '
    else:
        return 'پرداخت نشده'
