from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Subject,Topic

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'discription']  # use actual field names 

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic # Assuming Topic is a model similar to Subject
        fields = ['id', 'title', 'deadline', 'status','subject_id']  # use actual field names


class addSubjectSerializer(serializers.Serializer):
    subjectTitle=serializers.CharField()
    description= serializers.CharField(allow_blank=True, required=False, default="")    

class addTopicSerializer(serializers.Serializer):
    subjectTitle = serializers.CharField()
    topicTitle = serializers.CharField()
    deadline = serializers.DateField()
    status = serializers.ChoiceField(choices=["not_started", "In progress", "Completed"], default="not_started")

class statusSerialzer(serializers.Serializer):
    status= serializers.CharField()
    topic_id=serializers.IntegerField()    