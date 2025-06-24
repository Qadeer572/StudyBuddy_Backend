from .models import FlashCardDeck, FlashCard, Answer, FlashCardReview, Quiz, QuizQuestion
from rest_framework import serializers
from django.contrib.auth.models import User

class FlashCardDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCardDeck
        fields = ['id','subject', 'name', 'is_shared', 'created_at','user_id']
        read_only_fields = ['id', 'created_at']

class adsDeckSerializer(serializers.Serializer):
    subject = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    
    