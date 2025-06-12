from django.contrib import admin
from .models import FlashCardDeck, FlashCard, Answer, FlashCardReview, Quiz, QuizQuestion


admin.site.register(FlashCardDeck)
admin.site.register(FlashCard)
admin.site.register(Answer)
admin.site.register(FlashCardReview)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)

