from django.contrib import admin
from .models import PomodoroSession, PromodroStat, Notes
# Register your models here.

admin.site.register(PomodoroSession)
admin.site.register(PromodroStat)
admin.site.register(Notes)