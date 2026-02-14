from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
    path('interviews/', include('interviews.urls')),
    path('lms/', include('lms.urls')),
    path('', include('quiz.urls')),  # Includes quiz urls at root level for simplicity (e.g. /quiz/)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
