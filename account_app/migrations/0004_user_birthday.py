# Generated by Django 4.2.4 on 2023-08-13 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0003_user_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='تاریخ تولد'),
        ),
    ]
