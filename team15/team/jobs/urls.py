from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('my-jobs/', views.hr_jobs, name='hr_jobs'),
    path('list/', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('screening-preview/<int:resume_id>/<int:job_id>/', views.screening_preview, name='screening_preview'),
    path('confirm-apply/<int:resume_id>/<int:job_id>/', views.confirm_apply, name='confirm_apply'),
    path('screening/<int:pk>/', views.screening_result, name='screening_result'),
    path('<int:pk>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:pk>/status/<str:status>/', views.update_status, name='update_status'),
    path('applications/', views.my_applications, name='my_applications'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
]
