
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Job

try:
    job = Job.objects.get(pk=2)
    with open('job_2_skills.txt', 'w', encoding='utf-8') as f:
        f.write(f"Job 2 Skills: {repr(job.skills_required)}\n")
        
    print("Dumped Job 2 skills to job_2_skills.txt")
except Job.DoesNotExist:
    print("Job 2 not found")
