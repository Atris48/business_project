# Generated by Django 4.2.4 on 2023-08-16 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0008_userlogininfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='email',
        ),
        migrations.RemoveField(
            model_name='otp',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='otp',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='otp',
            name='password2',
        ),
    ]
