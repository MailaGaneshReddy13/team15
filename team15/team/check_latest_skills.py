import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application
from jobs.views import calculate_skills_match, extract_skills_list

app = Application.objects.last()
if not app:
    print("No application found.")
    exit()

# Redirect output to file
with open("skills_out_native.txt", "w", encoding="utf-8") as f:
    def log(msg):
        print(msg)
        f.write(str(msg) + "\n")

    log(f"--- APP ID: {app.id} ---")
    log(f"Job Title: {app.job.title}")
    log(f"Job Skills Required (Raw): '{app.job.skills_required}'")

    if app.resume:
        resume_skills = app.resume.parsed_data.get('Skills', [])
        log(f"Resume Skills (Raw): {resume_skills}")
    else:
        log("No resume.")

    log(f"App Matched Skills (DB): '{app.skills_matched}'")
    log(f"App Missing Skills (DB): '{app.missing_skills}'")

    # Recalculate
    if app.resume:
        r_skills = app.resume.parsed_data.get('Skills', [])
        j_skills = app.job.skills_required
        
        extracted_j = extract_skills_list(j_skills)
        log(f"Extracted Job Skills: {extracted_j}")
        
        matched, missing = calculate_skills_match(r_skills, j_skills)
        log(f"Calculated Matched: {matched}")
        log(f"Calculated Missing: {missing}")

