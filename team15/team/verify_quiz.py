import os
import django
import sys

# Setup Django environment
sys.path.append('c:/Users/DELL/Downloads/team/team')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from quiz.models import QuizAttempt
from ai_utils.utils import generate_quiz_questions
from django.contrib.auth import get_user_model

User = get_user_model()

def run_verification():
    with open('verification_log.txt', 'w') as f:
        f.write("Verifying Quiz Feature...\n")

        # 1. Test Model Creation
        try:
            print("Creating user and quiz attempt...")
            user, created = User.objects.get_or_create(username='test_quiz_user', email='test@example.com')
            attempt = QuizAttempt.objects.create(
                user=user,
                topic='Python',
                score=25,
                total_questions=30
            )
            f.write(f"PASS: QuizAttempt created: {attempt}\n")
        except Exception as e:
            f.write(f"FAIL: Model creation failed: {e}\n")

        # 2. Test Gemini API Integration (Mock or Real)
        try:
            f.write("Testing generate_quiz_questions...\n")
            print("Generating questions...")
            questions = generate_quiz_questions("Django Framework")
            if len(questions) == 30:
                f.write(f"PASS: Generated {len(questions)} questions.\n")
                if questions:
                    f.write(f"Sample Question: {questions[0]['question']}\n")
            else:
                f.write(f"FAIL: Expected 30 questions, got {len(questions)}\n")
        except Exception as e:
            f.write(f"FAIL: generate_quiz_questions failed: {e}\n")

if __name__ == "__main__":
    run_verification()
