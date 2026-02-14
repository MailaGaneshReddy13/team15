import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

def create_sample_data():
    # 1. Create or get an HR user
    hr, created = User.objects.get_or_create(
        username='hr_admin',
        email='hr@example.com',
        defaults={'role': 'hr', 'is_staff': True}
    )
    if created:
        hr.set_password('admin123')
        hr.save()
        print("Created HR user: hr_admin / admin123")

    # 2. Create sample jobs
    sample_jobs = [
        {
            'title': 'Junior Python Developer',
            'description': 'We are looking for a Python developer to build web applications using Django. You should be familiar with REST APIs and SQL.',
            'skills_required': 'Python, Django, SQL, Git',
            'experience_required': '0-2 years',
            'location': 'New York (Remote)'
        },
        {
            'title': 'Senior Frontend Engineer',
            'description': 'Looking for a React expert to design and implement interactive user interfaces. Proficiency in CSS and modern JS is a must.',
            'skills_required': 'React, JavaScript, CSS, HTML5, Webpack',
            'experience_required': '5+ years',
            'location': 'San Francisco'
        },
        {
            'title': 'Data Scientist',
            'description': 'Analyze large datasets and build machine learning models to solve business problems. Experience with Pandas and Scikit-learn is required.',
            'skills_required': 'Python, Pandas, Machine Learning, Statistics',
            'experience_required': '3+ years',
            'location': 'London (Hybrid)'
        }
    ]

    for job_data in sample_jobs:
        Job.objects.get_or_create(
            hr=hr,
            title=job_data['title'],
            defaults=job_data
        )
        print(f"Created job: {job_data['title']}")

if __name__ == '__main__':
    create_sample_data()
