from django.contrib import admin
from django.urls import path,include
from . import views 
from Dashboard.views import getFlashCardStats,getSubjectProgress,avergaeMarksInQuizBySubject
urlpatterns = [
    path('getFlashCardStats/',views.getFlashCardStats.as_view(),name="Get Flashcard Stats"),
    path('getSubjectProgress/',views.getSubjectProgress.as_view(),name="Get Subject Progress"),
    path('avergaeMarksInQuizBySubject/',views.avergaeMarksInQuizBySubject.as_view(),name="Average Marks in Quiz by Subject")
]
