import os
import django
import sys
import json

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from ai_utils.utils import generate_quiz_questions
from jobs.models import Resume
from django.contrib.auth import get_user_model

def test_view_logic():
    User = get_user_model()
    # Iterate all users to find one with a resume
    for user in User.objects.all():
        print(f"Checking user: {user.username}")
        latest_resume = Resume.objects.filter(candidate=user).order_by('-uploaded_at').first()
        
        if latest_resume:
            print(f"Resume FOUND for: {user.username}")
            resume_data = latest_resume.parsed_data
            
            # Debugging the data
            if resume_data:
                 print(f"Data type: {type(resume_data)}")
                 try:
                     print(f"Data dump: {json.dumps(resume_data)[:100]}...") # Print first 100 chars
                 except Exception as e:
                     print(f"JSON Dump FAILED: {e}")
            
            try:
                topic = "Python"
                print(f"Generating questions for topic: {topic} WITH resume data")
                questions = generate_quiz_questions(topic, resume_data=resume_data)
                print(f"Questions generated: {len(questions)}")
                break # Stop after one success
            except Exception as e:
                print("CRASH DETECTED during generation!")
                import traceback
                traceback.print_exc()
                break

if __name__ == "__main__":
    test_view_logic()
