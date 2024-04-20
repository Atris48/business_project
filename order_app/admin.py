from django.contrib import admin
from . import models

admin.site.register(models.Order)
admin.site.register(models.Discount)
admin.site.register(models.Support)
admin.site.register(models.SupportPlan)
admin.site.register(models.ExtendSupportPlan)
