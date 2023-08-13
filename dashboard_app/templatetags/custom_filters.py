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
