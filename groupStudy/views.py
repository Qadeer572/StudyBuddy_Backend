from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GroupCreationSerializer,AddMemberSerializer,groupSerializer,addGroupTaskSerializer,sharedStudyPlannerSerializer,AddSharedStudyPlannerSerializer,getMemberSerializer
from django.contrib.auth.models import User
from .models import StudyGroup,GroupMemberShip,SharedStudyPlanner,GroupTask
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

class getSharedStudyPlanner(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = request.user
        
        # Get all groups the user is part of
        user_groups = GroupMemberShip.objects.filter(user_id=user).values_list('group_id', flat=True)
        
        # Get shared planners in those groups
        shared_planners = SharedStudyPlanner.objects.filter(group_id__in=user_groups)

        if not shared_planners.exists():
            return Response({
                "status": True,
                "data": {},
                "message": "You have no shared study planners"
            })

        data = []
        for planner in shared_planners:
            data.append({
                "id": planner.id,
                "topicDiscription": planner.topicDiscription,
                "dueDate": planner.dueDate,
                "status": planner.status,
                "created_by": planner.created_by.username,
                "group_id": planner.group_id.id,
            })

        return Response({
            "status": True,
            "data": data,
            "message": "Shared study planners retrieved successfully"
        })

class getGroupTask(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user
        
        # Get all groups the user is part of
        user_groups = GroupMemberShip.objects.filter(user_id=user).values_list('group_id', flat=True)
        
        # Get tasks in those groups
        group_tasks = GroupTask.objects.filter(group_id__in=user_groups)

        if not group_tasks.exists():
            return Response({
                "status": True,
                "data": {},
                "message": "You have no tasks in any group"
            })

        data = []
        for task in group_tasks:
            data.append({
                "id": task.id,
                "task_name": task.task_name,
                "due_date": task.due_date,
                "assigned_to": task.assigned_to.username,
                "group_id": task.group_id.id,
                "complexity": task.complexity,
                "is_done": task.is_done
            })

        return Response({
            "status": True,
            "data": data,
            "message": "Group tasks retrieved successfully"
        })
    


class addGroupTask(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer = addGroupTaskSerializer(data=request.data)
        print(request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": {},
                "message": "Data is not valid"
            })

        serializer.save()

        return Response({
            "status": True,
            "data": {},
            "message": "Task added successfully"
        })    
    

 

class addStudyPlanne(APIView):
    permission_classes = [IsAuthenticated]

    print("chawan")
    def post(self, request):
        serializer = AddSharedStudyPlannerSerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({
                "status": False,
                "data": serializer.errors,
                "message": "Data is not valid"
            }, status=400)

        serializer.save()

        return Response({
            "status": True,
            "data": {},
            "message": "Shared study planner added successfully"
        })


class getUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=getMemberSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": {},
                "message": "Data is not valid"
            }, status=400)
        
         
        users = GroupMemberShip.objects.filter(group_id=serializer.validated_data['group_id'])
        data = []
        for user in users:
            data.append({
                "id": user.user_id.id,
                "username": user.user_id.username,
            })
        print(data)    
        return Response({
            "status": True,
            "data": data,
            "message": "Users retrieved successfully"
        })    