from django.contrib import admin
from django.urls import path,include
from .import views
from PromordoTimer.views import updatePromodroSession,addNotes,getSetting,updatSetting,getNotes,deleteNotes
urlpatterns = [
  path('updatePromodro/',views.updatePromodroSession.as_view(),name="updatePromodro"),
  path('addNotes/',views.addNotes.as_view(),name="Add Notes"),
  path('getSetting/',views.getSetting.as_view(),name="getSetting"),
  path('updatSetting/',views.updatSetting.as_view(),name="updatSetting"),
  path('getNotes/',views.getNotes.as_view(),name="getNotes"),
  path('deleteNotes/',views.deleteNotes.as_view(),name="deleteNotes"),
]