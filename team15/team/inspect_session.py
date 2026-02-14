import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from interviews.models import InterviewSession
from django.contrib.auth import get_user_model

def inspect_sessions():
    User = get_user_model()
    print("Inspecting Interview Sessions:")
    
    for session in InterviewSession.objects.all():
        print(f"\nSession ID: {session.id} | Candidate: {session.candidate.username} | Job: {session.job.title}")
        print(f"Total Questions: {session.questions.count()}")
        print("First 3 Questions:")
        for q in session.questions.order_by('order')[:3]:
            print(f"  - {q.text}")

if __name__ == "__main__":
    inspect_sessions()
