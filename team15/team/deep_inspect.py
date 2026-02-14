import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

print("--- DEEP INSPECTION ---")
app = Application.objects.last()
if not app:
    print("No application found.")
    exit()

candidate = app.candidate
print(f"Candidate ID: {candidate.id}")
print(f"Username: '{candidate.username}'")
print(f"First Name: '{candidate.first_name}'")
print(f"Last Name: '{candidate.last_name}'")
print(f"Full Name (method): '{candidate.get_full_name()}'")

print("\n--- RESUME DATA ---")
if app.resume:
    skills = app.resume.parsed_data.get('Skills', [])
    print(f"Resume Skills Raw ({type(skills)}): {skills}")
    
print("\n--- APPLICATION DATA ---")
print(f"App Skills Matched: '{app.skills_matched}'")
print(f"App Missing Skills: '{app.missing_skills}'")

print("\n--- USERS CHECK ---")
for u in User.objects.all():
    if "{{" in u.username or "{{" in u.first_name or "{{" in u.last_name:
        print(f"WARNING: CORRUPTED USER: {u.username} - {u.first_name} {u.last_name}")

