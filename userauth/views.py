from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import JsonResponse

# Create your views here.

def login():
    return "Login page"


@api_view(['POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        print("Hello world")
        email=request.data.get('email')
        password=request.data.get('password')
        print(email)
        print(password)
        return JsonResponse ({'message' :"User Created Sucessfully"},status=status.HTTP_201_CREATED)
    return JsonResponse ({'error' : "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
    
