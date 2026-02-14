import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Lesson

print(f"Total Courses: {Course.objects.count()}")
print(f"Total Lessons: {Lesson.objects.count()}")

for c in Course.objects.all():
    print(f"- {c.title}: {c.modules.count()} modules, {c.total_lessons} lessons")
