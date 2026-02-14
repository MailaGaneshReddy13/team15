import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application
from ai_utils.utils import analyze_match

app = Application.objects.last()
if not app:
    print("No application found.")
    exit()

print(f"Updating AI Feedback for App #{app.id} - Candidate: {app.candidate.username}")

# Prepare data for analysis
resume_data = app.resume.parsed_data if app.resume else {}
job_desc = app.job.description

# Call the updated AI function
print("Contacting Gemini for enhanced analysis...")
analysis = analyze_match(resume_data, job_desc)

# Update fields
app.match_score = analysis.get('match_score', 0)
app.skills_matched = ", ".join(analysis.get('skills_matched', []))
app.missing_skills = ", ".join(analysis.get('missing_skills', []))
app.ai_feedback = analysis.get('ai_feedback', '')
app.improvement_suggestions = analysis.get('improvement_suggestions', '')

app.save()

print("\n--- NEW FEEDBACK ---")
print(app.ai_feedback)
print("\n--- NEW SUGGESTIONS ---")
print(app.improvement_suggestions)
print("\nDone.")
