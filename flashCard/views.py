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
        response = model.generate_content(
                f"""
            Generate 10 multiple-choice flashcards for the topic "{self.topicName}" in subject "{self.subjectName}".

            Each flashcard must include:
            - "question": The question text
            - "options": A list of exactly 4 distinct options (strings)
            - "answer": The correct answer — MUST be exactly one of the options
            - "explanation": A short explanation for why the answer is correct

            ⚠️ Important rules:
            - Only ONE correct answer is allowed.
            - "answer" must be a single string that exactly matches one of the values in the "options" list.
            - Do NOT include any markdown like ```json.
            - Format your response as a pure JSON array like this:
            [
            {{
                "question": "...",
                "options": ["...", "...", "...", "..."],
                "answer": "...",
                "explanation": "..."
            }},
            ...
            ]
            """
            )

        cleaned_output = self.clean_json_output(response.text)
        return cleaned_output
    

class getflashCards(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            deck = FlashCardDeck.objects.filter(user_id=request.user)
        except FlashCardDeck.DoesNotExist:
            return Response({
                "status": False,
                "error": "Deck not found"
            })
        flashcards = []
        for d in deck:
            cards = FlashCard.objects.filter(deck_id=d).values('id','deck_id', 'question', 'created_at', 'difficulty')
            flashcards.extend(cards)

        return Response({
            "status": True,
            "flashcards": list(flashcards)
        })


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
            dueCards=10,
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
        flashcard_objs = []  # To keep track of flashcards
        all_options = []     # To keep options in the same order

        for card in flashcards:
            question = card.get('question')
            options = card.get('options')
            answer = card.get('answer')
            explanation = card.get('explanation')

            if not question or not answer or not explanation or not options or answer not in options:
                return Response({
                    "status": False,
                    "error": "Invalid card format or answer not in options",
                    "card": card
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

            flashcard_objs.append(flashcard)
            all_options.append(options)  # Keep the options in order

        quiz = QuizCreation()
        quiz.generateQuiz(deck, flashcard_objs, all_options)


        return Response({
            "status": True,
            "message": "Deck and flashcards created successfully",
            "deck_id": deck.id
        })
    

class updatStatusCard(APIView):
    
    def post(self, request):
        try:
            deck = FlashCardDeck.objects.get(id=request.data['deck_id'])
        except FlashCardDeck.DoesNotExist:
            return Response({
                "status": False,
                "error": "Deck not found"
            })
        
        deck.dueCards = request.data['dueCards']
        deck.mastered = request.data['mastered']
        deck.learning = request.data['learning']
        deck.sucess_rate=request.data['sucess_rate']
        deck.lastStudied = date.today()
        deck.save()

        

        return Response({
            "status": True,
            "message": "Deck updated successfully"
        })

class QuizCreation():

    @staticmethod
    def generateQuiz(deck, flashcard_objs, all_options):
        quiz = Quiz.objects.create(
            user_id=deck.user_id,
            deck_id=deck,
            score=0.0,
            total_questions=len(flashcard_objs),
            created_at=date.today()
        )

        for i in range(len(flashcard_objs)):
            fc = flashcard_objs[i]
            options = all_options[i]
            try:
                QuizQuestion.objects.create(
                    quiz_id=quiz,
                    flashcard_id=fc,
                    question=fc.question,
                    options=options
                )
            except Exception as e:
                print(f"Failed to create quiz question for card {fc.id}: {str(e)}")
                continue

        return quiz


     
class getQuizes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user
        quizzes = Quiz.objects.filter(user_id=user_id).values(
            'id', 'deck_id__name', 'score', 'total_questions', 'created_at'
        )

        return Response({
            "status": True,
            "quizzes": list(quizzes)
        })