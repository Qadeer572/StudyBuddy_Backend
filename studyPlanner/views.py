from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers  import addSubjectSerializer,addTopicSerializer,SubjectSerializer,TopicSerializer,statusSerialzer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Subject,Topic
from datetime import date

 



class allSubjects(APIView):
    def get(self, request):
        subjects = Subject.objects.filter(user_id=request.user)
        serializer = SubjectSerializer(subjects, many=True)
        return Response({
            "status": True,
            "subjects": serializer.data,
            "message": "Subjects retrieved successfully"
        })


class allTopics(APIView):
    def get(self,request):     
        topics = Topic.objects.filter(subject_id__user_id=request.user)
        serializer = TopicSerializer(topics, many=True)
        return Response({
            "status": True,
            "topics": serializer.data,
            "message": "Topics retrieved successfully"
        })


class addSubject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = addSubjectSerializer(data=request.data)

        if not serializer.is_valid():
            print("Not valid")
            return Response({
                "status": False,
                "error": serializer.errors
            })

        title = serializer.validated_data["subjectTitle"]
        description = serializer.validated_data["description"]

        # Optionally check for duplicate subject names
        if Subject.objects.filter(name=title, user_id=request.user).exists():
            return Response({
                "status": False,
                "error": "Subject with this name already exists"
            })

        # Create the subject, associating it with the authenticated user
        subject = Subject(
            name=title,
            discription=description,
            user_id=request.user , # Associate with the authenticated user
            created_at=date.today()
        )
        print(request.user)
        subject.save()

        return Response({
            "status": True,
            "data": {},  # Use lowercase 'data' for consistency
            "message": "Subject added successfully"
        })
    

class addTopic(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received Data",request.data)
        serializer = addTopicSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": False,
                "error": serializer.errors
            })

        subject_title = serializer.validated_data["subjectTitle"]
        topic_title = serializer.validated_data["topicTitle"]
        deadline = serializer.validated_data["deadline"]
        status = serializer.validated_data["status"]

        # Find the subject by title and associate it with the authenticated user
        try:
            subject = Subject.objects.get(name=subject_title, user_id=request.user)
        except Subject.DoesNotExist:
            return Response({
                "status": False,
                "error": "Subject does not exist"
            })

        # Create the topic, associating it with the subject and authenticated user
        topic = Topic(
            subject_id=subject,
            title=topic_title,
            deadline=deadline,
            status=status,
            created_at=date.today()
        )
        topic.save()

        return Response({
            "status": True,
            "data": {},  # Use lowercase 'data' for consistency
            "message": "Topic added successfully"
        })
    

class updateTopicStatus(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=statusSerialzer(data=request.data)
        print(request.data)

        if not serializer.is_valid():
            return Response ({
                "status" : False,
                 "data"  : {},
                 "message": "data is not valie"
            })
        
        status=serializer.validated_data['status']
        topic_id=serializer.validated_data['topic_id']

        topic=Topic.objects.get(id=topic_id)
        if topic:
            topic.status=status
            topic.created_at=date.today()
            topic.save()


            return Response({
                "status":True,
                "data":{},
                "message":"status updated successfully"
            })

        return Response({
            "status": False,
            "data": {},
            "message": "Topic does not exist"
        })    