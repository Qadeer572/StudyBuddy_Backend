# Generated by Django 5.1.7 on 2025-06-26 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PromordoTimer', '0004_alter_pomodorosession_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pomodorosession',
            name='audioNotification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pomodorosession',
            name='autoStart',
            field=models.BooleanField(default=True),
        ),
    ]
