from django.db.models import Q
from account_app.models import UserLoginCount
from contact_us_app.models import CompanyInfo
from dashboard_app.models import Notification
from price_app.models import PriceCategory
from ticket_app.models import Chat


def notification_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.order_by('-created_at')
        return {"notifications": notifications}
    else:
        return {"None": None}


def notification_count(request):
    if request.user.is_authenticated:
        count = 0
        notifications = Notification.objects.filter(Q(user=request.user) | Q(user=None))
        for notification in notifications:
            if request.user not in notification.remove.all():
                count += 1
        return {"notifications_count": count}
    else:
        return {"None": None}


def plan_categories(request):
    plan_categories = PriceCategory.objects.all()
    return {"plan_categories": plan_categories}


def company_info(request):
    return {'info': CompanyInfo.objects.first()}


def visit_count(request):
    if request.user.is_authenticated:
        if UserLoginCount.objects.filter(user=request.user).exists():
            user_login_count = UserLoginCount.objects.get(user=request.user).count
            return {'user_login_count': user_login_count}
        else:
            return {'user_login_count': 0}
    else:
        return {"user_login_count": 0}


def is_admin_replied(request):
    if request.user.is_authenticated:
        if Chat.objects.filter(user=request.user).exists():
            chat = Chat.objects.get(user=request.user)
            reply = chat.is_replied
            return {'is_reply': reply}
        else:
            return {'is_reply': False}
    else:
        return {'is_reply': False}
