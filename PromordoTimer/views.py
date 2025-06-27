from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from studyPlanner.models import Subject
from datetime import date
from .models import PomodoroSession,Notes

class updatePromodroSession(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user

        promodro=PomodoroSession.objects.filter(user=user).first()

        if not promodro:
            return Response({
                "status": False,
                 "message": "Promodro Session does not exist"
            })
        
        workDuration=request.data.get("workDuration")
        shortBreak=request.data.get("shortBreak")
        longBreak=request.data.get("longBreak")
        autoStart=request.data.get("autoStart")
        audioNotification=request.data.get("audioNotification")

        promodro.workDuration=workDuration
        promodro.shortBreak=shortBreak
        promodro.longBreak=longBreak
        promodro.autoStart=autoStart
        promodro.audioNotification=audioNotification

        promodro.save()

        return Response({
            "status" : True,
            "data": {
                "workDuration": workDuration,
                "shortBreak":shortBreak,
                "longBreak":longBreak,
                "autoStart" :autoStart,
                "audioNotification" :audioNotification

            }
        })
    
class addNotes(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user
        promodro=PomodoroSession.objects.filter(user=user).first()
        if not promodro:
            return Response({
                "status": False,
                 "error" : "Promodro Does not Exist"
            })
        notesContent=request.data.get("notesContent")
        notes=Notes.objects.create(
            promodro_id=promodro,
            content=notesContent,
        )
        notes.save()

        return Response({
            "status": True,
             "data": {
                 "id": notes.id,
                  "promodro_id":notes.promodro_id.id,
                  "content": notes.content
             },
             "message": "Notes added Successfully"
        })

class getSetting(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        promodro=PomodoroSession.objects.filter(user=user).first()

        if not promodro:
            return Response({
                "status": False,
                "message": "Promodro Session does not exist"
            })

        return Response({
            "status": True,
            "data": {
                "workDuration": promodro.workDuration,
                "shortBreak": promodro.shortBreak,
                "longBreak": promodro.longBreak,
                "autoStart": promodro.autoStart,
                "audioNotification": promodro.audioNotification
            }
        })
    
class updatSetting(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user
        promodro=PomodoroSession.objects.filter(user=user).first()
        if not promodro:
            return Response({
                "status": False,
                "message": "Promodro Session does not exist"
            })
        workDuration = request.data.get("workDuration")
        shortBreak = request.data.get("shortBreak")
        longBreak = request.data.get("longBreak")
        autoStart = request.data.get("autoStart")
        audioNotification = request.data.get("audioNotification")

        promodro.workDuration = workDuration
        promodro.shortBreak = shortBreak
        promodro.longBreak = longBreak
        promodro.autoStart = autoStart
        promodro.audioNotification = audioNotification
        promodro.save()

        return Response({
            "status": True,
            "message": "Settings updated successfully",
            "data": {
                "workDuration": promodro.workDuration,
                "shortBreak": promodro.shortBreak,
                "longBreak": promodro.longBreak,
                "autoStart": promodro.autoStart,
                "audioNotification": promodro.audioNotification
            }
        })   

class getNotes(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        user = request.user
        promodro = PomodoroSession.objects.filter(user=user).first()

        if not promodro:
            return Response({
                "status": False,
                "message": "Promodro Session does not exist"
            })

        notes = Notes.objects.filter(promodro_id=promodro)

        notes_data = [
            {
                "id": note.id,
                "text": note.content,
                "timestamp": note.created_at
            } for note in notes
        ]

        return Response({
            "status": True,
            "data": notes_data
        })

class deleteNotes(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user
        promodro=PomodoroSession.objects.filter(user=user).first()
        if not promodro:
            return Response({
                "status": False,
                "message": "Promodro Session does not exist"
            })
        note_id = request.data.get("id")
        try:
            note = Notes.objects.get(id=note_id, promodro_id=promodro)
            note.delete()
            return Response({
                "status": True,
                "message": "Note deleted successfully"
            })
        except Notes.DoesNotExist:
            return Response({
                "status": False,
                "message": "Note does not exist"
            })
           