import os
import django
import sys
import time

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from ai_utils.utils import generate_interview_questions

def test_generation_with_retry():
    print("Testing generate_interview_questions with RETRY logic...")
    print("This might take a few seconds due to potential backoff...")
    
    resume_data = {"Skills": ["Python", "Django"], "Experience": "3 Years"}
    job_title = "Python Developer"
    
    start_time = time.time()
    questions = generate_interview_questions(resume_data, job_title)
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if questions and "Aptitude Q1" in questions[0]:
        print("FAILURE: Still returned Fallback Mock Data after retries.")
    else:
        print(f"SUCCESS: Generated {len(questions)} AI Questions.")
        print(f"First Question: {questions[0]}")

if __name__ == "__main__":
    test_generation_with_retry()
