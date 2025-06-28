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

class signup(APIView):

    def post(self,request):
        first_name = request.data.get("firstName")
        last_name = request.data.get("lastName")
        email = request.data.get("email")
        password = request.data.get("password")
        if not first_name or not last_name or not email or not password:
            return Response({
                "status": False,
                "error": "All fields are required"
            }, status=400)
        if User.objects.filter(email=email).exists():
            return Response({
                "status": False,
                "error": "Email already exists"
            }, status=400)
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        return Response({
            "status": True,
            "message": "User registered successfully",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password  # Note: Do not return password in production
            }
        })