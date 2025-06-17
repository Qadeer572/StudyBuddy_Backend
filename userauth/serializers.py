from rest_framework import serializers

from django.contrib.auth.models import User

class userSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class addSubjectSerializer(serializers.Serializer):
    name=serializers.CharField()
    description= serializers.CharField()    