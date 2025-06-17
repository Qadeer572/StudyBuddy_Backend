from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import loginSerializer

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