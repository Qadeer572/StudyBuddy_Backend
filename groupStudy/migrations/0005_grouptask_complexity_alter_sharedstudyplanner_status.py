# Generated by Django 5.1.7 on 2025-06-23 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupStudy', '0004_sharedstudyplanner_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouptask',
            name='complexity',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Low', max_length=20),
        ),
        migrations.AlterField(
            model_name='sharedstudyplanner',
            name='status',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started', max_length=20),
        ),
    ]
