from django.contrib import admin
from django.urls import path,include
from .import views
from userauth.views import userLogin,setDefaultTimer
urlpatterns = [
    path('login/', views.userLogin.as_view(), name='login'),
    path('signup/',views.signup,name='signup'),
    path('setDefaultTimer/', views.setDefaultTimer.as_view(), name='setDefaultTimer'),
   # path('users/', userApiview.as_view(), name='user-list'),
     
]