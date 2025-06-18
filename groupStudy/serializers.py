from rest_framework import serializers
import string
import random
from datetime import date
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import StudyGroup,GroupMemberShip


class AddMemberSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=10, required=True)
    role = serializers.ChoiceField(required=False,allow_blank=True,choices=["ADMIN", "MEMBER"], default="MEMBER")

    def validate_invite_code(self, value):
        if not StudyGroup.objects.filter(invite_code=value).exists():
            raise ValidationError("Invalid invite code.")
        return value
    
    def validate_role(self, value):
        if value not in ["ADMIN", "MEMBER"]:
            value="MEMBER"
        return value

    def create(self, validated_data):
        code = validated_data.pop('invite_code')  # remove invite_code from data
        group = StudyGroup.objects.get(invite_code=code)

        user = self.context['request'].user
        # Create new member
        new_member = GroupMemberShip.objects.create(
            group_id=group,
            user_id=user,
            role=validated_data['role']
        )
        return new_member


class GroupStudySerializer(serializers.ModelSerializer):
    class meta:
        model = StudyGroup
        fields = ['id', 'name', 'invite_code', 'created_by', 'created_at']

class GroupCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    invite_code = serializers.CharField(max_length=10, required=False)
    

    def validate_invite_code(self,value):
        if not value:
            return None
        return value
    
    def generate_inivite_code(self,length=6):
        return ''.join(random.choices(string.ascii_uppercase+string.digits,k=length))
    
    def create(self, validated_data):

        if not validated_data.get('invit_code'):
            validated_data['invite_code']=self.generate_inivite_code(6)
        
        while StudyGroup.objects.filter(invite_code=validated_data['invite_code']).exists():
            validated_data['invite_code'] = self.generate_invite_code() 

        validated_data['created_by']=self.context['request'].user
        request1=self.context['request']
        #validated_data['created_at']=date.today() 

        
              

        group_study = StudyGroup.objects.create(**validated_data)
        code=validated_data['invite_code']
        serializer = AddMemberSerializer(data={"invite_code": code, "role": "ADMIN"},context={'request': request1})
        
        if  serializer.is_valid():
            serializer.save()
        return group_study      
    