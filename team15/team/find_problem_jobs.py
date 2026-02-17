
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Job

print("Searching for jobs with '{{' in skills...")
found = False
with open('problem_jobs.txt', 'w', encoding='utf-8') as f:
    for job in Job.objects.all():
        if '{{' in job.skills_required:
            found = True
            msg = f"Job {job.id} has problematic skills: {repr(job.skills_required)}"
            print(msg)
            f.write(msg + "\n")

if not found:
    print("No jobs with '{{' found.")
    with open('problem_jobs.txt', 'w', encoding='utf-8') as f:
        f.write("No jobs with '{{' found.\n")
