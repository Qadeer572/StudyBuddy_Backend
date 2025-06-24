from django.contrib import admin
from django.urls import path,include
from . import views 
from flashCard.views import addCardDeck,getDecks
urlpatterns = [
    path('addCardDeck/',views.addCardDeck.as_view(),name="addDeck"),
    path('getDecks/',views.getDecks.as_view(),name="getDecks"),
]
