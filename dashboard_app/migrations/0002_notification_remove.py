# Generated by Django 4.2.4 on 2023-08-13 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='remove',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
