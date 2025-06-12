from django.contrib import admin
from .models import StudyGroup,GroupMemberShip,GroupMessage

# Register your models here.

admin.site.register(StudyGroup)
admin.site.register(GroupMemberShip)
admin.site.register(GroupMessage)
