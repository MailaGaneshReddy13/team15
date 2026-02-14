import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application, Resume
from django.contrib.auth import get_user_model

User = get_user_model()

log_file = open("corruption_log.txt", "w", encoding="utf-8")

def log(msg):
    print(msg)
    log_file.write(msg + "\n")

def clean_text(text):
    if not text:
        return text
    if "{{" in text or "}}" in text:
        cleaned = text.replace("{{", "").replace("}}", "").replace("app.candidate.get_full_name|default:app.candidate.username", "").strip()
        return cleaned
    return text

log("--- STARTING AGGRESSIVE CLEANUP ---")

# 1. Clean Users
for u in User.objects.all():
    dirty = False
    if "{{" in u.username:
        log(f"Fixing Username: {u.username}")
        u.username = clean_text(u.username) or f"user_{u.id}"
        dirty = True
    if "{{" in u.first_name:
        log(f"Fixing First Name: {u.first_name}")
        u.first_name = clean_text(u.first_name)
        dirty = True
    if "{{" in u.last_name:
        log(f"Fixing Last Name: {u.last_name}")
        u.last_name = clean_text(u.last_name)
        dirty = True
        
    if dirty:
        u.save()

# 2. Clean Applications
for app in Application.objects.all():
    dirty = False
    
    # Skills Matched
    if app.skills_matched and ("{{" in app.skills_matched or "skill" in app.skills_matched.lower()):
        log(f"Fixing App {app.id} Matched Skills: {app.skills_matched}")
        clean = clean_text(app.skills_matched)
        # remove 'skill' word
        parts = [s.strip() for s in clean.split(',')]
        clean = ", ".join([p for p in parts if p.lower() not in ['skill', 'skills', '']])
        app.skills_matched = clean
        dirty = True

    # Missing Skills
    if app.missing_skills and ("{{" in app.missing_skills or "skill" in app.missing_skills.lower()):
        log(f"Fixing App {app.id} Missing Skills: {app.missing_skills}")
        clean = clean_text(app.missing_skills)
        parts = [s.strip() for s in clean.split(',')]
        clean = ", ".join([p for p in parts if p.lower() not in ['skill', 'skills', '']])
        app.missing_skills = clean
        dirty = True

    # Improvement Suggestions
    if app.improvement_suggestions and "{{" in app.improvement_suggestions:
        log(f"Fixing App {app.id} Suggestions: {app.improvement_suggestions}")
        app.improvement_suggestions = clean_text(app.improvement_suggestions)
        dirty = True
        
    if dirty:
        app.save()

# 3. Clean Resumes
for res in Resume.objects.all():
    data = res.parsed_data
    if data and 'Skills' in data:
        skills = data['Skills']
        new_skills = []
        changed = False
        if isinstance(skills, list):
            for s in skills:
                if "{{" in s or "}}" in s or s.lower() in ['skill', 'skills']:
                    clean_s = clean_text(s)
                    if clean_s and clean_s.lower() not in ['skill', 'skills']:
                        new_skills.append(clean_s)
                    changed = True
                else:
                    new_skills.append(s)
        
        if changed:
            log(f"Fixing Resume {res.id} Skills: {skills} -> {new_skills}")
            data['Skills'] = new_skills
            res.parsed_data = data
            res.save()

# 4. Clean Jobs
from jobs.models import Job
for job in Job.objects.all():
    if job.skills_required and ("{{" in job.skills_required or "}}" in job.skills_required):
         log(f"Fixing Job {job.id} Skills: {job.skills_required}")
         job.skills_required = clean_text(job.skills_required)
         job.save()

log("--- CLEANUP COMPLETE ---")
log_file.close()
