import os
import django
import sys
import json

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from ai_utils.utils import generate_interview_questions

def test_interview_generation():
    print("Testing generate_interview_questions...")
    
    # Mock resume data
    resume_data = {
        "Skills": ["Python", "Django", "Rest API"],
        "Experience": "3 years as Backend Developer",
        "Education": "B.Tech in CS"
    }
    job_title = "Python Developer"
    
    try:
        questions = generate_interview_questions(resume_data, job_title)
        print(f"Generated {len(questions)} questions.")
        
        # Check if they are sample questions
        is_sample = any("Aptitude Q1" in q for q in questions)
        if is_sample:
            print("FAILURE: Returned Mock/Sample questions!")
        else:
            print("SUCCESS: Returned AI questions!")
            print("First 3 questions:")
            for q in questions[:3]:
                print(f"- {q}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_interview_generation()
