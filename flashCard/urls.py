from django.contrib import admin
from django.urls import path,include
from . import views 
from flashCard.views import addCardDeck,getDecks,getflashCards,updatStatusCard,getQuizes
urlpatterns = [
    path('addCardDeck/',views.addCardDeck.as_view(),name="addDeck"),
    path('getDecks/',views.getDecks.as_view(),name="getDecks"),
    path('getflashCards/',views.getflashCards.as_view(),name="getflashCards"),
    path('updatStatusCard/',views.updatStatusCard.as_view(),name="updatStatusCard"),
    path('getQuizes/',views.getQuizes.as_view(),name="getQuizes"),
]
