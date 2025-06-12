from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.

class PomodoroSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=25)  # Duration in minutes

    def __str__(self):
        return f"Session {self.id} for {self.user.username} - {'Completed' if self.is_completed else 'In Progress'}"
