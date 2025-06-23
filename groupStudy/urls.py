from django.contrib import admin
from django.urls import path,include
from . import views 
from groupStudy.views import createGroup,joinGroup,getGroups,getSharedStudyPlanner,getGroupTask,addGroupTask,addStudyPlanne,getUser
urlpatterns = [
    path('createGroup/',views.createGroup.as_view(),name="createGroup"),
    path('joinGroup/',views.joinGroup.as_view(),name="joinGroup"),
    path('getGroups/',views.getGroups.as_view(),name="getGroups"),
    path('getStudyPlanner/',views.getSharedStudyPlanner.as_view(),name="sharedStudyPlanner"),
    path('getGroupTask/',views.getGroupTask.as_view(),name="getGroupTasks"),
    path('addGroupTask/',views.addGroupTask.as_view(),name="addGroupTask"),
    path('addStudyPlanner/',views.addStudyPlanne.as_view(),name="addStudyPlanner"),
    path('getGroupUser/',views.getUser.as_view(),name="getUser"),
 
]

