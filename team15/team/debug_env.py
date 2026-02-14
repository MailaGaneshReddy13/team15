import sys
try:
    import django
    django_version = django.get_version()
except ImportError:
    django_version = "Not installed"

with open("debug_info.txt", "w", encoding="utf-8") as f:
    f.write(f"Python executable: {sys.executable}\n")
    f.write(f"Python version: {sys.version}\n")
    f.write(f"Django version: {django_version}\n")
