from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from datetime import date
from flashCard.models import FlashCardDeck,FlashCard,Quiz,QuizQuestion
from studyPlanner.models import Subject,Topic
from django.db import models


class getFlashCardStats(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        decks=FlashCardDeck.objects.filter(user_id=user)
        if not decks.exists():
            return Response({
                "status": True,
                "message": "No flashcard decks found for the user."
            }, status=404)
        
        total_card=decks.count()
        total_card*=10

        mastered=decks.aggregate(models.Sum('mastered'))['mastered__sum'] or 0
        learning=decks.aggregate(models.Sum('learning'))['learning__sum'] or 0
        due_cards=decks.aggregate(models.Sum('dueCards'))['dueCards__sum'] or 0
        
        stats={
            "total_cards": total_card,
            "mastered": mastered,
            "learning": learning,
            "due_cards": due_cards,
        }
        return Response({
            "status": True,
            "message": "Flashcard stats fetched successfully.",
            "data": stats
        })

class getSubjectProgress(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        subjects=Subject.objects.filter(user_id=user)
        if not subjects.exists():
            return Response({
                "status": True,
                "message": "No subjects found for the user."
            }, status=404)
        subject_progress = []
        for subject in subjects:
            topics = Topic.objects.filter(subject_id=subject)
            total_topics = topics.count()
            completed_topics = topics.filter(status="COMPLETED").count()
            progress = (completed_topics / total_topics * 100) if total_topics > 0 else 0
            
            subject_progress.append({
                "subject_id": subject.id,
                "subject_name": subject.name,
                "total_topics": total_topics,
                "completed_topics": completed_topics,
                "progress": progress
            })

        return Response({
            "status": True,
            "message": "Subject progress fetched successfully.",
            "data": subject_progress
        })      

class avergaeMarksInQuizBySubject(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        quizzes=Quiz.objects.filter(user_id=user)
        if not quizzes.exists():
            return Response({
                "status": True,
                "message": "No quizzes found for the user."
            }, status=404)
        
        subject_scores = {}
        for quiz in quizzes:
            deck = quiz.deck_id
            subject = deck.subject
            
            if subject not in subject_scores:
                subject_scores[subject] = {
                    "total_score": 0,
                    "quiz_count": 0
                }
            
            subject_scores[subject]["total_score"] += quiz.score
            subject_scores[subject]["quiz_count"] += 1
        
        average_scores = {subject.name: (data["total_score"] / data["quiz_count"]) if data["quiz_count"] > 0 else 0 
                          for subject, data in subject_scores.items()}
        
        return Response({
            "status": True,
            "message": "Average marks in quizzes by subject fetched successfully.",
            "data": average_scores
        })          