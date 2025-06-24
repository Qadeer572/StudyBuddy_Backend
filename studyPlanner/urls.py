from django.contrib import admin
from django.urls import path,include
from . import views 
from studyPlanner.views import addSubject,addTopic,allSubjects,allTopics,updateTopicStatus
urlpatterns = [
    path('addSubject/',views.addSubject.as_view(),name="addSubject"),
    path('addTopic/',views.addTopic.as_view(),name="addTopic"),
    path('allSubjects/',views.allSubjects.as_view(),name="allSubject"),
    path('allTopics/',views.allTopics.as_view(),name="allTopics"),
    path('updateStatus/',views.updateTopicStatus.as_view(),name="updateStatus"),
]
