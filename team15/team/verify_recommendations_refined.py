
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.views import get_recommended_courses
from ai_utils.utils import analyze_match
from lms.models import Course

# Ensure some courses exist
if not Course.objects.exists():
    print("Creating dummy courses...")
    Course.objects.create(title="Intro to Python", description="Learn Python basics", category="technical")
    Course.objects.create(title="Django for Beginners", description="Build web apps with Django", category="technical")
    Course.objects.create(title="Advanced Docker", description="Containerization with Docker", category="technical")

# Test 1: Missing skills that match courses
missing_skills = ["Docker", "Python"]
print(f"Testing with missing skills: {missing_skills}")
courses = get_recommended_courses(missing_skills)
print(f"Recommended Courses ({len(courses)}): {[c.title for c in courses]}")

# Test 2: Missing skills with no direct match (fallback removed)
missing_skills_fallback = ["NonExistentSkill"]
print(f"Testing with missing skills (strict mode): {missing_skills_fallback}")
courses_fallback = get_recommended_courses(missing_skills_fallback)
print(f"Recommended Courses (should be empty): {[c.title for c in courses_fallback]}")

# Test 3: Analyze Match with missing skills
print("Testing analyze_match with missing skills...")
try:
    result = analyze_match({}, "Job Desc", missing_skills=["Docker"])
    print("Analyze match executed successfully.")
except Exception as e:
    print(f"Analyze match failed: {e}")
