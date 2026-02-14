import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from jobs.models import Application

app = Application.objects.last()
if app:
    print(f"FEEDBACK:\n{app.ai_feedback}\n\nSUGGESTIONS:\n{app.improvement_suggestions}")
else:
    print("No application found.")
