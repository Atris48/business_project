# Generated by Django 4.2.4 on 2023-08-21 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket_app', '0002_chat_is_finished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
