# Generated by Django 5.1.7 on 2025-06-26 06:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PromordoTimer', '0002_remove_pomodorosession_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pomodorosession',
            old_name='duration',
            new_name='workDuration',
        ),
        migrations.AddField(
            model_name='pomodorosession',
            name='longBreak',
            field=models.PositiveIntegerField(default=15, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='pomodorosession',
            name='shortBreak',
            field=models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
