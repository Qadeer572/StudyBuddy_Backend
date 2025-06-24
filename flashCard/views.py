from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import FlashCardDeck, FlashCard, Answer, FlashCardReview, Quiz, QuizQuestion
from .serilaizers import adsDeckSerializer,FlashCardDeckSerializer
from rest_framework.response import Response
from studyPlanner.models import Subject
from datetime import date
import json

import google.generativeai as genai

genai.configure(api_key="AIzaSyCmS2TuyUXfXRREsiEEgmWeG8Plu__0SqA")


# Create your views here.
model = genai.GenerativeModel('gemini-1.5-flash-latest')

class getDecks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user
        ser = FlashCardDeck.objects.filter(user_id=user_id).values(
            'id', 'subject__name', 'name','cardCount','dueCards','mastered','learning', 'is_shared', 'created_at','lastStudied'
        )
        return Response({
            "status": True,
            "decks":  ser
        })
class generatCard():
    def __init__(self, topicName, subjectName):
        self.topicName = topicName
        self.subjectName = subjectName
    @staticmethod
    def clean_json_output(text):
    # Remove markdown code block ```json ... ```
        if text.startswith("```json"):
            text = text.lstrip("```json").strip()
        text = text.strip("` \n")  # removes trailing ```
        return text
    def generate(self):
        response = model.generate_content(f"Generate 10 questions and (answers with Explanation) on topic {self.topicName} of subject {self.subjectName} in the form of flashcards. Each question should be unique and cover different aspects of the topic. The questions should be suitable for a quiz format, and the answers should be detailed enough to provide a clear understanding of the topic. The response should be in JSON format with 'question', 'answer', and 'explanation' fields for each flashcard.")
        cleaned_output = self.clean_json_output(response.text)
        return cleaned_output
    
    
    


class addCardDeck(APIView):

    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.data)
        serializer=adsDeckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "error": serializer.errors
            })
 
       
                
        subject = Subject.objects.get(id=serializer.validated_data["subject"])
        name =   serializer.validated_data["name"]
        is_shared = False
        user_id= request.user
        created_at= date.today()

        deck=FlashCardDeck.objects.filter(name=name, subject=subject, user_id=user_id)
        if deck.exists():
            return Response({
                "status": False,
                "error": "Deck with this name already exists"
            })
        deck = FlashCardDeck(
            subject=subject,
            name=name,
            is_shared=is_shared,
            user_id=user_id,
            cardCount=10,
            lastStudied=date.today(),
            created_at=created_at
        )
        deck.save()

        topicName = serializer.validated_data["name"]
        subjectName = Subject.objects.get(id=serializer.validated_data["subject"]).name
        card_generator = generatCard(topicName, subjectName)
        generated_cards = card_generator.generate()
        
        print('Generated Card:\n',generated_cards)
        try:
            flashcards = json.loads(generated_cards)
        except json.JSONDecodeError as e:
            return Response({
                "status": False,
                "error": f"Failed to decode generated cards: {str(e)}",
                "raw_output": generated_cards
            })
        
        for card in flashcards:
            question = card.get('question')
            answer = card.get('answer')
            explanation = card.get('explanation')

            if not question or not answer or not explanation:
                return Response({
                    "status": False,
                    "error": "Invalid card format received from the generator"
                })

            flashcard = FlashCard(
                deck_id=deck,
                question=question,
                created_at=date.today()
            )
            flashcard.save()
            answer_obj = Answer(
                card_id=flashcard,
                answer=answer,
                explanation=explanation
            )
            answer_obj.save()

        return Response({
            "status": True,
            "message": "Deck created successfully",
            "deck_id": deck.id
        })