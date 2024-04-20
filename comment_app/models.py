from django.db import models
from account_app.models import User
from django_jalali.db import models as jmodels


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.fullname
