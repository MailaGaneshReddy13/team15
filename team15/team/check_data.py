import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application, Job

app = Application.objects.last()
if app:
    print(f"Application ID: {app.id}")
    print(f"Job Title: {app.job.title}")
    print(f"Job Skills Required: {app.job.skills_required}")
    
    if app.resume:
        print(f"Resume Parsed Data (Keys): {app.resume.parsed_data.keys()}")
        print(f"Resume Skills: {app.resume.parsed_data.get('Skills')}")
        print(f"Resume Skills Type: {type(app.resume.parsed_data.get('Skills'))}")
    else:
        print("No resume linked.")
        
    # Check what calculate_skills_match returns
    from jobs.views import calculate_skills_match
    resume_skills = app.resume.parsed_data.get('Skills', []) if app.resume else []
    matched, missing = calculate_skills_match(resume_skills, app.job.skills_required)
    print(f"Calculated Matched: {matched}")
    print(f"Calculated Missing: {missing}")
else:
    print("No applications found.")
