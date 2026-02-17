
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.views import extract_skills_list
from jobs.models import Job

print("--- Debugging Skills ---")

# Specific check for Job 3 (from user URL)
try:
    job = Job.objects.get(pk=3)
    print(f"Job ID: 3, Title: {job.title}")
    raw_skills = job.skills_required
    print(f"Raw Skills (repr): {repr(raw_skills)}")
    
    extracted = extract_skills_list(raw_skills)
    print(f"Extracted (repr): {repr(extracted)}")
    
except Job.DoesNotExist:
    print("Job 3 not found.")

print("\n--- Testing extract_skills_list ---")
test_cases = [
    "{{ skill }}",
    "{{ skill }}, Java",
    "{{skill}}",
    "{ { skill } }",
    "{{  skill  }}"
]

for t in test_cases:
    res = extract_skills_list(t)
    print(f"Input: '{t}' -> Output: {res}")
