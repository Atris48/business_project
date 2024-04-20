from django.db import models
from django_jalali.db import models as jmodels


class PortfolioCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    category = models.ManyToManyField(PortfolioCategory)
    title = models.CharField(max_length=200)
    url = models.URLField()
    image = models.ImageField(upload_to='portfolio/image')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return self.title
