# Generated by Django 4.2.4 on 2023-08-20 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0013_remove_support_applied_discount_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='applied_discount_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='support',
            name='is_discount_applied',
            field=models.BooleanField(default=False, verbose_name='کد تخفیف اعمال شده'),
        ),
    ]
