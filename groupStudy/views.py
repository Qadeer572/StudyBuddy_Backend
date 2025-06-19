from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GroupCreationSerializer,AddMemberSerializer,groupSerializer
from django.contrib.auth.models import User
from .models import StudyGroup,GroupMemberShip
from datetime import date
# Create your views here.

class getGroups(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user
        groups_data = GroupMemberShip.objects.filter(user_id=user)
        if not groups_data.exists():
            return Response({
                "status": False,
                "data": {},
                "message": "You are not a member of any group"
            })
        
        groups = []
        for group in groups_data:
            group_info = StudyGroup.objects.get(id=group.group_id.id)
            serializer = groupSerializer(group_info)
            groups.append(serializer.data)

         
        return Response({
            "status": True,
            "data": groups,
            "message": "Groups retrieved successfully"
        })

class createGroup(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print(request.data)
        serializer=GroupCreationSerializer(data=request.data, context={'request':request})

        if not serializer.is_valid():
            return Response({
                "status": False,
                "data" : {},
                "message": "data is not Valid"
            })
        name=serializer.validated_data['name']
        group= StudyGroup.objects.filter(name=name,created_by=request.user)

        if group:
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
        group= StudyGroup.objects.get(invite_code=serializer.validated_data['invite_code'])
        
        member=GroupMemberShip.objects.filter(group_id=group,user_id=request.user)

        if member:
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