from django.contrib import admin
from .models import StudyGroup,GroupMemberShip,GroupMessage,SharedStudyPlanner,GroupTask

# Register your models here.

admin.site.register(StudyGroup)
admin.site.register(GroupMemberShip)
admin.site.register(GroupMessage)
admin.site.register(SharedStudyPlanner)
admin.site.register(GroupTask)
