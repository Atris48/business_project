# Generated by Django 4.2.4 on 2023-08-15 00:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('percentage', models.PositiveIntegerField()),
                ('is_expired', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'کد تخفیف ها',
                'verbose_name_plural': 'کد تخفیف',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('applied_discount_code', models.CharField(blank=True, max_length=20, null=True)),
                ('is_discount_applied', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True, null=True)),
                ('tracking_code', models.CharField(max_length=200)),
                ('is_paid', models.BooleanField(default=False)),
                ('preparation_template', models.BooleanField(default=False)),
                ('preparing', models.BooleanField(default=False)),
                ('thirty_five_percent_ready', models.BooleanField(default=False)),
                ('seventy_percent_ready', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'سفارشات',
                'verbose_name_plural': 'سفارش',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plane_name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('website_type', models.CharField(max_length=100)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order_app.order')),
            ],
            options={
                'verbose_name': 'سفارشات',
                'verbose_name_plural': 'سفارش ها',
            },
        ),
    ]