# Generated by Django 5.1.7 on 2025-06-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashCard', '0003_flashcard_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcarddeck',
            name='sucess_rate',
            field=models.FloatField(default=0.0),
        ),
    ]
