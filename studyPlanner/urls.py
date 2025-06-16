from django.contrib import admin
from django.urls import path,include
from . import views 
from studyPlanner.views import addSubject
urlpatterns = [
    path('addSubject/',views.addSubject.as_view(),name="addSubject"),
]