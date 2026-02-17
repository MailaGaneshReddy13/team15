
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Job

print("Dumping All Jobs Skills:")
for job in Job.objects.all():
    print(f"Job {job.id}: {repr(job.skills_required)}")
