from rest_framework import serializers

from django.contrib.auth.models import User

class userSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class loginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password=serializers.CharField()