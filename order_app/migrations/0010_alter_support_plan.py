# Generated by Django 4.2.4 on 2023-08-17 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0009_alter_support_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supports', to='order_app.supportplan'),
        ),
    ]
