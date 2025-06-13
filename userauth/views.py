from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User

from django.http import JsonResponse

# Create your views here.

def login():
    return "Login page"


@api_view(['POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        firstName=request.data.get('firstName')
        lastName=request.data.get('lastName')
        email=request.data.get('email')
        password=request.data.get('password')

         
        if not firstName or not lastName or not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user= User.objects.create_user(
            username=email,
            first_name=firstName,
            last_name=lastName,
            email=email,
            password=password
        )
        
        user.save()

        return JsonResponse ({'message' :"User Created Sucessfully"},status=status.HTTP_201_CREATED)
    return JsonResponse ({'error' : "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
    
