from django.db import models


class PriceCategory(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Ability(models.Model):
    title = models.CharField(max_length=400)

    def __str__(self):
        return self.title


class Price(models.Model):
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
    ability = models.ManyToManyField(Ability)
    category = models.ManyToManyField(PriceCategory)

    def __str__(self):
        return self.name
