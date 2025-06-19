from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from studyPlanner.models import Subject,Topic

class StudyGroup(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    invite_code=models.CharField(max_length=10, unique=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.TimeField(null=True)
    def __str__(self):
        return self.name
    
class roleChoice(models.TextChoices):
    ADMIN='ADMIN','Admin'
    MEMBER='MEMBER','Member'


class   GroupMemberShip(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    group_id=models.ForeignKey(StudyGroup,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=roleChoice.choices,default=roleChoice.MEMBER)
    joined_at=models.TimeField(null=True)

    def __str__(self):
        return str(self.id)

class GroupMessage(models.Model):
    id=models.AutoField(primary_key=True)
    group_id=models.ForeignKey(StudyGroup,on_delete=models.CASCADE)
    sender_id=models.ForeignKey(User,on_delete=models.CASCADE)    
    content=models.TextField()
    sent_at=models.TimeField()


    def __str__(self):
        return self.id

    