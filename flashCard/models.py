from django.db import models
from django.contrib.auth.models import User
from studyPlanner.models import Subject
from django.core.validators import MinValueValidator, MaxValueValidator


class FlashCardDeck(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    cardCount=models.IntegerField(default=0, validators=[MinValueValidator(0)])
    dueCards=models.IntegerField(default=0, validators=[MinValueValidator(0)])
    mastered= models.IntegerField(default=0, validators=[MinValueValidator(0)])
    learning= models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_shared=models.BooleanField(default=False)
    sucess_rate=models.FloatField(default=0.0)
    lastStudied=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Answer(models.Model):
    id=models.AutoField(primary_key=True)
    card_id=models.ForeignKey('FlashCard', on_delete=models.CASCADE, related_name='answers')
    answer=models.TextField()
    explanation=models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer for card {self.card_id.id}"
        
class FlashCard(models.Model):
    id=models.AutoField(primary_key=True)
    deck_id=models.ForeignKey(FlashCardDeck, on_delete=models.CASCADE, related_name='cards')
    question=models.TextField()
    difficulty=models.CharField(max_length=20, choices=[
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard')
    ], default='Medium')
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Card {self.id} in deck {self.deck_id.name}"


class FlashCardReview(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard_id=models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    last_reviewed_at=models.DateTimeField(auto_now=True)
    next_review_at=models.DateTimeField()
    sucess_rate=models.FloatField(default=0.0)

    def __str__(self):
        return f"Review for card {self.flashcard_id.id} by user {self.user_id.username}"
    

class Quiz(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    deck_id=models.ForeignKey(FlashCardDeck, on_delete=models.CASCADE)
    score=models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    total_questions=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Quiz for card {self.deck_id_id} by user {self.user_id.username}"
    
class QuizQuestion(models.Model):
    id=models.AutoField(primary_key=True)
    quiz_id=models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question=models.TextField()
    flashcard_id=models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    user_answer=models.TextField(blank=True, null=True)
    is_correct=models.BooleanField(default=False)
    options=models.JSONField(blank=True, null=True)  # To store multiple choice options if needed

    def __str__(self):
        return f"Question {self.id} for quiz {self.quiz_id.id}"   
    
     
