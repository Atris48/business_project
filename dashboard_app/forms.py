from django import forms

from order_app.models import Order, Support, SupportPlan, ExtendSupportPlan
from price_app.models import Price
from .models import Notification, Announcement


class CreateNotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('user', 'title', 'description', 'url')


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'description', 'url')


class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class EditSupportOrderForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = "__all__"


class OrderPrice(forms.ModelForm):
    class Meta:
        model = Price
        fields = "__all__"


class SupportPriceForm(forms.ModelForm):
    class Meta:
        model = SupportPlan
        fields = "__all__"


class ExtendSupportPlanForm(forms.ModelForm):
    class Meta:
        model = ExtendSupportPlan
        fields = "__all__"
