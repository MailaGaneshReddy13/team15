import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hr_agent.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
print(f"User count: {User.objects.count()}")
