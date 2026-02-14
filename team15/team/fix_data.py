import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from interviews.models import Notification, LiveInterview
from jobs.models import Application
from django.contrib.auth import get_user_model

def fix_notifications():
    User = get_user_model()
    candidates = User.objects.filter(role='candidate')
    hr = User.objects.filter(role='hr').first()
    
    for candidate in candidates:
        app = Application.objects.filter(candidate=candidate).first()
        if app and hr:
            # Create a test live interview if one doesn't exist
            interview, _ = LiveInterview.objects.get_or_create(
                application=app,
                interviewer=hr,
                defaults={
                    'scheduled_at': '2026-02-16 14:00:00',
                    'meeting_id': f'meeting-{candidate.username}-{app.id}'
                }
            )
            # Update notifications to link to this interview
            count = Notification.objects.filter(
                recipient=candidate, 
                notification_type='interview_scheduled'
            ).update(related_interview=interview)
            print(f"Updated {count} notifications for {candidate.username} with interview {interview.meeting_id}")

if __name__ == '__main__':
    fix_notifications()
