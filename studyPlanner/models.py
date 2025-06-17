from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class Subject (models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    discription=models.TextField(blank=True,null=True)
    created_at= models.DateTimeField()

    def __str__(self):
        return self.name


class StatusChoices(models.TextChoices):
    NOT_STARTED = 'NOT_STARTED', 'Not Started'
    COMPLETED = 'COMPLETED', 'Completed'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'

class Topic(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subject, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    deadline=models.DateField()
    status = models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.NOT_STARTED)
    created_at=models.DateField()

    def __str__(self):
        return self.title