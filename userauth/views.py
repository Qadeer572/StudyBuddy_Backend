from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import loginSerializer
from rest_framework.permissions import IsAuthenticated
from PromordoTimer.models import PomodoroSession, PromodroStat, Notes

class userLogin(APIView):
    def post(self, request):
        serializer = loginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "error": serializer.errors
            })

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
            user_obj = authenticate(username=user.username, password=password)
            if user_obj:
                token, _ = Token.objects.get_or_create(user=user_obj)
                return Response({
                    "status": True,
                    "message": "Login successful",
                    "token": str(token)
                })
            else:
                return Response({
                    "status": False,
                    "error": "Invalid credentials"
                })
        except User.DoesNotExist:
            return Response({
                "status": False,
                "error": "Invalid credentials"
            })


 
def signup(request):
     return "Signup function"



class setDefaultTimer(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user

        workDuration = 25
        shortBreak = 5
        longBreak = 15
        autoStart = True
        audioNotification = True

        promodro= PomodoroSession.objects.filter(user=request.user).first()
        
        if not promodro:
            promodro = PomodoroSession.objects.create(
                user=user,
                workDuration=workDuration,
                shortBreak=shortBreak,
                longBreak=longBreak,
                autoStart=autoStart,
                audioNotification=audioNotification
            )
        else:
            promodro.workDuration = workDuration
            promodro.shortBreak = shortBreak
            promodro.longBreak = longBreak
            promodro.autoStart = autoStart
            promodro.audioNotification = audioNotification
            promodro.save()

        return Response({
            "status": True,
            "message": "Default timer settings updated successfully",
            "data": {
                "workDuration": promodro.workDuration,
                "shortBreak": promodro.shortBreak,
                "longBreak": promodro.longBreak,
                "autoStart": promodro.autoStart,
                "audioNotification": promodro.audioNotification
            }
        })        