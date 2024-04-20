# Generated by Django 4.2.4 on 2023-08-17 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('price_app', '0003_remove_price_category_price_category'),
        ('order_app', '0006_alter_order_is_discount_applied_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('tracking_code', models.CharField(max_length=30)),
                ('applied_discount_code', models.CharField(blank=True, max_length=20, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('is_discount_applied', models.BooleanField(default=False, verbose_name='کد تخفیف اعمال شده')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('is_expiration', models.BooleanField(default=False)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('pay_at', django_jalali.db.models.jDateTimeField(blank=True, null=True)),
                ('expiration_date', django_jalali.db.models.jDateTimeField()),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supports', to='price_app.price')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
