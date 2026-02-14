import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application, Resume

def clean_braces(text):
    if not text:
        return text
    # aggressive cleanup of template tags if they got saved as text
    cleaned = text.replace('{{', '').replace('}}', '').strip()
    return cleaned

print("Sanitizing Database...")
for app in Application.objects.all():
    changed = False
    
    # Check if name fields somehow got corrupted (unlikely but checking)
    
    # Check skills
    if app.skills_matched and ('{{' in app.skills_matched or 'skill' in app.skills_matched.lower()):
        print(f"Sanitizing App {app.id} matched skills: {app.skills_matched}")
        app.skills_matched = clean_braces(app.skills_matched)
        # remove 'skill' word again
        parts = [s.strip() for s in app.skills_matched.split(',')]
        app.skills_matched = ", ".join([p for p in parts if p.lower() not in ['skill', 'skills', '']])
        changed = True
        
    if app.missing_skills and ('{{' in app.missing_skills or 'skill' in app.missing_skills.lower()):
        print(f"Sanitizing App {app.id} missing skills: {app.missing_skills}")
        app.missing_skills = clean_braces(app.missing_skills)
        parts = [s.strip() for s in app.missing_skills.split(',')]
        app.missing_skills = ", ".join([p for p in parts if p.lower() not in ['skill', 'skills', '']])
        changed = True

    if changed:
        app.save()
        print(f"Saved App {app.id}")

from django.contrib.auth import get_user_model
User = get_user_model()
for user in User.objects.all():
    if user.first_name and '{{' in user.first_name:
        print(f"Fixing User Name {user.username}")
        user.first_name = ""
        user.last_name = ""
        user.save()

print("Sanitization Clean Complete.")
