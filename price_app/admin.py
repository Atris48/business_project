from django.contrib import admin
from . import models

admin.site.register(models.PriceCategory)
admin.site.register(models.Price)
admin.site.register(models.Ability)
