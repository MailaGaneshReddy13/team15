from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.quiz_home, name='quiz_home'),
    path('quiz/history/', views.quiz_history, name='quiz_history'),
    path('api/quiz/questions/', views.get_quiz_questions, name='get_quiz_questions'),
    path('api/quiz/submit/', views.submit_quiz_result, name='submit_quiz_result'),
]
