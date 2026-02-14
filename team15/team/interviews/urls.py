from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:application_id>/', views.start_interview, name='mock_interview'),
    path('question/<int:session_id>/', views.get_question, name='get_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('report/<int:session_id>/', views.interview_report, name='interview_report'),
    path('finish/<int:session_id>/', views.finish_interview, name='finish_interview'),
    path('schedule-live/<int:application_id>/', views.schedule_live_interview, name='schedule_live_interview'),
    path('live/<str:meeting_id>/', views.live_interview_room, name='live_interview_room'),
    
    # AI Interview Routes
    path('ai-setup/', views.ai_interview_setup, name='ai_interview_setup'),
    path('ai-start/', views.start_ai_interview, name='start_ai_interview'),
    path('ai-room/<int:session_id>/', views.ai_interview_room, name='ai_interview_room'),
    path('ai-chat/<int:session_id>/', views.chat_with_interviewer, name='chat_with_interviewer'),
    path('ai-process/<int:session_id>/', views.process_ai_feedback, name='process_ai_feedback'),
    path('ai-report/<int:session_id>/', views.ai_interview_report, name='ai_interview_report'),
    path('delete-session/<int:session_id>/', views.delete_interview_session, name='delete_interview_session'),
    path('delete-ai-session/<int:session_id>/', views.delete_ai_interview_session, name='delete_ai_interview_session'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]
