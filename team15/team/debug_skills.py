
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.views import extract_skills_list, calculate_skills_match
from jobs.models import Job

# Test extract_skills_list logic
test_str = "{{ skill }}, {{ Skill }}, Python, {{ skill }}"
print(f"Testing string: '{test_str}'")
extracted = extract_skills_list(test_str)
print(f"Extracted: {extracted}")

test_list = ["{{ skill }}", "Java", "{{ Skill }}"]
print(f"Testing list: {test_list}")
extracted_list = extract_skills_list(test_list)
print(f"Extracted List: {extracted_list}")

# Check Jobs in DB
print("\nChecking Jobs in DB:")
for job in Job.objects.all():
    print(f"Job ID: {job.id}, Title: {job.title}")
    print(f"Skills Required Raw: '{job.skills_required}'")
    extracted_job_skills = extract_skills_list(job.skills_required)
    print(f"Skills Extracted: {extracted_job_skills}")
    print("-" * 20)

