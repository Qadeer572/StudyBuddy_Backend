from rest_framework import serializers
import string
import random
from datetime import date
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import StudyGroup,GroupMemberShip,GroupTask,SharedStudyPlanner

class groupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'invite_code','created_by','created_at']


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


        
class sharedStudyPlannerSerializer(serializers.Serializer):
    class Meta:
        model = SharedStudyPlanner
        fields = ['id', 'group_id', 'topicDiscription','status', 'dueDate', 'created_by']

 

class addGroupTaskSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    task_name = serializers.CharField(max_length=100)
    due_date = serializers.DateField()
    assigned_to = serializers.CharField(max_length=100, required=True)
    complexity = serializers.ChoiceField(
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('Hard', 'Hard')],
        required=True
    )
    is_done = serializers.BooleanField(default=False, required=False)

    def validate_group_id(self, value):
        if not StudyGroup.objects.filter(id=value).exists():
            raise ValidationError("Invalid group ID.")
        return value
    
    def validate_assign_to(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise ValidationError("Assigned user does not exist.")

        # Optional: check if user is in the group
        group_id = self.initial_data.get('group_id')
        if group_id and not GroupMemberShip.objects.filter(user_id=user, group_id=group_id).exists():
            raise ValidationError("Assigned user is not a member of the group.")

        return value

    def create(self, validated_data):
        group = StudyGroup.objects.get(id=validated_data['group_id'])

        assigned_user = None
        if 'assigned_to' in validated_data:
            assigned_user = User.objects.get(username=validated_data['assigned_to'])
        print("Assigned User:", assigned_user)
        task = GroupTask.objects.create(
            group_id=group,
            task_name=validated_data['task_name'],
            due_date=validated_data['due_date'],
            assigned_to=assigned_user,
            complexity=validated_data['complexity'],
            is_done=validated_data['is_done']
        )
        return task


 

class AddSharedStudyPlannerSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    topicDiscription = serializers.CharField(max_length=500)
    dueDate = serializers.DateField()

    def validate_group_id(self, value):
        if not StudyGroup.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid group ID.")
        return value

    def create(self, validated_data):
        return SharedStudyPlanner.objects.create(
            group_id=StudyGroup.objects.get(id=validated_data['group_id']),
            topicDiscription=validated_data['topicDiscription'],
            dueDate=validated_data['dueDate'],
            created_by=self.context['request'].user
        )


class getMemberSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()