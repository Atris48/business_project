from datetime import timedelta
import jalali_date
from django import template
import jdatetime

register = template.Library()
from jdatetime import datetime as jdatetime


@register.filter()
def get_time_ago(date):
    now = jdatetime.now()

    # Convert 'date' to offset-naive datetime by removing timezone information
    date_naive = date.replace(tzinfo=None)

    time_difference = now - date_naive

    # Calculate the total number of minutes, hours, and days
    total_minutes = (time_difference.days * 24 * 60) + (time_difference.seconds // 60)
    if total_minutes == 0:
        time_ago_string = f"لحظاتی پیش"
    elif total_minutes < 60:
        time_ago_string = f"{total_minutes} دقیقه پیش"
    elif total_minutes < 1440:  # 1440 minutes in a day
        total_hours = total_minutes // 60
        time_ago_string = f"{total_hours} ساعت پیش"
    else:
        total_days = time_difference.days
        time_ago_string = f"{total_days} روز پیش"

    return time_ago_string


@register.filter()
def get_last_message(dict):
    return dict['content']


@register.filter()
def get_last_role(dict):
    return dict['role']
