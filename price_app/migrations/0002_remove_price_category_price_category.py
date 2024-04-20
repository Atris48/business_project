# Generated by Django 4.2.4 on 2023-08-15 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('price_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='category',
        ),
        migrations.AddField(
            model_name='price',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='price_app.pricecategory'),
        ),
    ]
