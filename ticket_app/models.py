from django.db import models
from django.db.models import JSONField
from account_app.models import User
from django_jalali.db import models as jmodels


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat')
    messages_history = JSONField(default=[], null=True, blank=True)
    is_replied = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.phone)
