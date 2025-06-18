from django.contrib import admin
from django.urls import path,include
from . import views 
from groupStudy.views import createGroup,joinGroup
urlpatterns = [
    path('createGroup/',views.createGroup.as_view(),name="createGroup"),
    path('joinGroup/',views.joinGroup.as_view(),name="joinGroup"),
 
]