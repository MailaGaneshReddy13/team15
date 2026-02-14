import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from interviews.models import InterviewSession
from jobs.models import Application

def trigger_visit():
    User = get_user_model()
    # Find a user with a session
    for session in InterviewSession.objects.all():
        print(f"Testing Session: {session.id} for user {session.candidate.username}")
        
        # Check if it has mock questions currently
        first_q = session.questions.order_by('order').first()
        print(f"Current First Question: {first_q.text if first_q else 'None'}")
        
        if not first_q:
            print("Skipping empty session.")
            continue

        # Find the application ID to build the URL
        app = Application.objects.filter(job=session.job, candidate=session.candidate).first()
        if not app:
            print("No application found for this session.")
            continue
            
        url = f"/interviews/start/{app.id}/"
        print(f"Visiting URL: {url}")
        
        client = Client()
        client.force_login(session.candidate)
        response = client.get(url)
        print(f"Response Status: {response.status_code}")
        
        # Verify if changed
        session.refresh_from_db()
        new_first_q = session.questions.order_by('order').first()
        print(f"New First Question: {new_first_q.text if new_first_q else 'None'}")
        
        if new_first_q and new_first_q.text != first_q.text:
             print("SUCCESS: Questions regenerated!")
             break
        else:
             print("NO CHANGE.")

if __name__ == "__main__":
    trigger_visit()
