from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime



# Create your models here.

class PomodoroSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=True)
    workDuration = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=25)  # Duration in minutes
    shortBreak= models.PositiveIntegerField(validators=[MinValueValidator(1)], default=5)  # Duration in minutes
    longBreak = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=15)  # Duration in minutesyth
    autoStart = models.BooleanField(default=True)  # Auto-start next session
    audioNotification = models.BooleanField(default=True)  # Audio notification for session end

    def __str__(self):
        return f"Session {self.id} for {self.user.username}"


class PromodroStat(models.Model):
    id = models.AutoField(primary_key=True)
    promodro_id=models.ForeignKey(PomodoroSession, on_delete=models.CASCADE,related_name='promodro_stats')
    totalSession = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # Total number of sessions
    completed = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # Number of completed sessions
    date= models.DateField(default=timezone.now)  # Date of the stat
    day = models.CharField(max_length=10, editable=False)

    def save(self, *args, **kwargs):
        if not self.day:
            self.day = datetime.now().strftime('%A')  # e.g., "Thursday"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Stat {self.id} for {self.user.username} - {'Completed' if self.completed else 'In Progress'}"


class Notes(models.Model):
    id= models.AutoField(primary_key=True)
    promodro_id = models.ForeignKey(PomodoroSession, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)  # Timestamp when the note was created

    def __str__(self):
        return f"Note {self.id} for Session {self.promodro_id.id} - Created at {self.created_at}"
    
    