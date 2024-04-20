from django.db import models
from django_jalali.db import models as jmodels


class TeamCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    image = models.ImageField(upload_to='team/images')
    number_of_project = models.PositiveIntegerField(default=0)
    work_experience = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField(TeamCategory, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
