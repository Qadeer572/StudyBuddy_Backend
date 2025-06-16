from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Subject
 

class addSubjectSerializer(serializers.Serializer):
    title=serializers.CharField()
    description= serializers.CharField()    