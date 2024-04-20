from django.db import models


class ServiceCategory(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    category = models.ManyToManyField(ServiceCategory)


    def __str__(self):
        return self.title
