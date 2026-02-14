import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from ai_utils.utils import generate_quiz_questions

def test_quiz_generation():
    topic = "Python"
    print(f"Testing quiz generation for topic: {topic}")
    questions = generate_quiz_questions(topic)
    
    print(f"Generated {len(questions)} questions")
    if len(questions) > 0:
        print("First question sample:")
        print(questions[0])
    else:
        print("NO QUESTIONS GENERATED!")

if __name__ == "__main__":
    test_quiz_generation()
