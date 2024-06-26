# Generated by Django 4.2.4 on 2023-08-15 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0005_remove_order_preparation_template_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_discount_applied',
            field=models.BooleanField(default=False, verbose_name='کد تخفیف اعمال شده'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='کامل شده'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='پرداخت شده'),
        ),
    ]
