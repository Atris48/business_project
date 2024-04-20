from django.db import models
from django_jalali.db import models as jmodels

from account_app.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    remove = models.ManyToManyField(User, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=300, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=300, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
