from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Subject
 

class addSubjectSerializer(serializers.Serializer):
    subjectTitle=serializers.CharField()
    description= serializers.CharField(allow_blank=True, required=False, default="")    