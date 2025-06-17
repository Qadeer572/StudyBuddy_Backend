from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers  import addSubjectSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Subject
from datetime import date

 



 

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