import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Module, Lesson, UserCourseProgress

print(f"Deleting {UserCourseProgress.objects.count()} progress records...")
UserCourseProgress.objects.all().delete()

print(f"Deleting {Lesson.objects.count()} lessons...")
Lesson.objects.all().delete()

print(f"Deleting {Module.objects.count()} modules...")
Module.objects.all().delete()

print(f"Deleting {Course.objects.count()} courses...")
Course.objects.all().delete()

print("LMS data wiped clean.")
