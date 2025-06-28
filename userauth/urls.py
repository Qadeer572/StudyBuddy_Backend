from django.contrib import admin
from django.urls import path,include
from .import views
from userauth.views import userLogin,setDefaultTimer,signup
urlpatterns = [
    path('login/', views.userLogin.as_view(), name='login'),
    path('signup/',views.signup.as_view(),name='signup'),
    path('setDefaultTimer/', views.setDefaultTimer.as_view(), name='setDefaultTimer'),
   # path('users/', userApiview.as_view(), name='user-list'),
     
]