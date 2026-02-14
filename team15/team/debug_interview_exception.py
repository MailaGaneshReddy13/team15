import os
import django
import sys
import json
import time

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from ai_utils.utils import generate_interview_questions

def debug_error():
    print("Attempting to generate interview questions...")
    resume_data = {"Skills": ["Python", "Django"], "Experience": "3 Years"}
    job_title = "Python Developer"
    
    # The function prints exception details to stdout
    questions = generate_interview_questions(resume_data, job_title)
    
    if questions and "Aptitude Q1" in questions[0]:
        print("\nFAILURE: Returned Fallback Mock Data.")
        print("Check the output above for 'AI API Error'.")
    else:
        print("\nSUCCESS: Generated AI Questions.")
        print(questions[:2])

if __name__ == "__main__":
    debug_error()
