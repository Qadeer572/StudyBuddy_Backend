from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GroupCreationSerializer,GroupStudySerializer,AddMemberSerializer
from django.contrib.auth.models import User
from .models import StudyGroup,GroupMemberShip
from datetime import date
# Create your views here.


class createGroup(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        
        serializer=GroupCreationSerializer(data=request.data, context={'request':request})

        if not serializer.is_valid():
            return Response({
                "status": False,
                "data" : {},
                "message": "data is not Valid"
            })
        name=serializer.validated_data['name']
        group= StudyGroup.objects.filter(name=name,created_by=request.user)

        if group.exists:
            return Response({
                "status": False,
                "data"  : {},
                "message" : "This group is already Exists"
            })
        serializer.save()

        return Response({
            "status": True,
            "data" : {},
            "Message": "Group created Successful"
        })
    
class joinGroup(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer= AddMemberSerializer(data=request.data, context={'request':request})

        if not serializer.is_valid():
            return Response({
                "status": False,
                "data" : {},
                "message": "data is not Valid"
            })
        
        member=GroupMemberShip.objects.filter(user_id=request.user)

        if member.exists():
            return Response({
                "status": False,
                "data" : {},
                "message": "You are already a member of this group"
            })
        
        serializer.save()

        return Response({
            "status": True,
            "Data": {},
            "Message": "You have joined the group successfully"
        })    