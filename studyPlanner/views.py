from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # Not used anymore
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .models import Subject, Topic
from django.http import JsonResponse
from datetime import date

@api_view(['POST'])
def addSubject(request):
    title = request.data.get('subjectTitle')
    description = request.data.get('description')

    if not title:
        return JsonResponse({'error': 'Please fill all fields'}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.is_authenticated:
        current_user = request.user
        subject = Subject(
            name=title,
            user_id=current_user,
            description=description,  # Fix spelling in model too
            created_at=date.today()
        )
        subject.save()
        return JsonResponse({'success': 'Added successfully'}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
