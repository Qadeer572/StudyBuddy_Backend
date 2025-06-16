from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import userSerialzer,loginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



class userApiview(APIView):
     
     def get(self,request):
          querySet= User.objects.all()
          serializer = userSerialzer(querySet, many=True)
          return Response({
               'status': True,
               'data': serializer.data
          })
     


class userLogin(APIView):
     permission_classes = [IsAuthenticated]
     def post(self, request):
          data=request.data

          serializer= loginSerializer(data=data)

          if not serializer.is_valid():
               return Response({
                    "status": False,
                    "data" : serializer.errors
               })
          
          username=serializer.data["username"]
          password=serializer.data["password"]

          print(username,password)

          user_obj= authenticate(username=username,password=password)

          if user_obj:
               token,_= Token.objects.get_or_create(user=user_obj )
               return Response({
               "status": True,
               "data": {"token": str(token)}
          })
          
          return Response({
               "status": False,
               "data": {},
               "Message" : "Invalid Credentials"
          })
     


def login(request):
    return "Login function"


 
def signup(request):
     return "Signup function"