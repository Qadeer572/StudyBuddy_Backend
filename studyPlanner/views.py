from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers  import addSubjectSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Subject


class addSubject(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data= request.data

        serializer= addSubjectSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                "status" : False,
                 "data": serializer.errors
            })
        
        title=serializer.data("title")
        description=serializer.data("description")
        subject= Subject(
            name=title,
            discription=description
        )
        subject.save()

        return Response({
            "status" : True,
            "Data"   : {},
            "message": "Subject added Successfully"
        })