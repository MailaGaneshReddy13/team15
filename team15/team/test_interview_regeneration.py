import os
import django
import sys
import time

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from jobs.models import Job, Application, Resume
from interviews.models import InterviewSession, InterviewQuestion

def test_regeneration():
    User = get_user_model()
    # 1. Setup User and Data
    user = User.objects.first()
    if not user:
        print("No user found.")
        return

    print(f"Using user: {user.username}")
    
    # Ensure user has a resume
    resume, _ = Resume.objects.get_or_create(candidate=user, defaults={'file': 'test.pdf'})
    if not resume.parsed_data:
        resume.parsed_data = {"Skills": ["Python"], "Experience": "Test"}
        resume.save()

    # Create a dummy job
    hr_user = User.objects.filter(role='hr').first() or user
    job, _ = Job.objects.get_or_create(
        title="Test Job for Interview", 
        hr=hr_user,
        defaults={'description': 'Test', 'skills_required': 'Python', 'location': 'Remote', 'experience_required': '1 year'}
    )
    
    # Create Application
    app, _ = Application.objects.get_or_create(job=job, candidate=user)
    app.resume = resume
    app.save()
    
    # 2. Create a Session with MOCK questions
    session, _ = InterviewSession.objects.get_or_create(candidate=user, job=job)
    session.questions.all().delete() # Clear any existing
    
    InterviewQuestion.objects.create(session=session, text="Aptitude Q1: Mock Question", order=1)
    InterviewQuestion.objects.create(session=session, text="Technical Q1: Mock Question", order=2)
    
    print(f"Seeded session with {session.questions.count()} mock questions.")
    print(f"First question: {session.questions.first().text}")
    
    # 3. Trigger View
    c = Client()
    c.force_login(user)
    
    url = f"/interviews/start/{app.id}/"
    print(f"Visiting {url}...")
    response = c.get(url)
    
    if response.status_code != 200:
        print(f"Error: Status {response.status_code}")
        return

    # 4. Verify Regeneration
    session.refresh_from_db()
    count = session.questions.count()
    first_q = session.questions.order_by('order').first().text
    
    print(f"Questions after visit: {count}")
    print(f"First question after visit: {first_q}")
    
    if count == 30 and not first_q.startswith("Aptitude Q1: Mock"):
        print("SUCCESS: Questions were regenerated!")
    elif first_q.startswith("Aptitude Q1: Mock"):
        print("FAILURE: Questions were NOT regenerated (still mock).")
    else:
        print(f"UNCERTAIN: Count={count}, First='{first_q}'")

if __name__ == "__main__":
    test_regeneration()
