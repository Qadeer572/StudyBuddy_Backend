from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AnalyticalSnapshot(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    study_minuts=models.IntegerField(default=0)
    topic_completed=models.IntegerField(default=0)
    flashcards_reviewed=models.IntegerField(default=0)
    avg_quiz_score=models.FloatField(default=0.0)

    def __str__(self):
        return "Snapshot by " + str(self.user_id)





