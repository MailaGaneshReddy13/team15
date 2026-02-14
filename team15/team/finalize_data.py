import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Module, Lesson
from interviews.models import Notification
from django.contrib.auth import get_user_model

def finalize_all_data():
    User = get_user_model()
    print("Seeding Additional LMS Content...")

    # 1. SQL Course
    sql_data = {
        'title': 'SQL & Database Fundamentals',
        'description': 'Master the language of data. Learn how to design, query, and manage relational databases.',
        'category': 'technical',
        'modules': [
            {
                'title': '1. Basic Queries',
                'lessons': [{'title': 'SELECT & FROM', 'duration': 15, 'content': '<h3>SELECT Basics</h3><p>SQL SELECT statement is used to fetch data from a database table.</p>'}]
            },
            {
                'title': '2. Joins & Relationships',
                'lessons': [{'title': 'INNER JOIN', 'duration': 25, 'content': '<h3>Joining Tables</h3><p>An INNER JOIN returns rows when there is at least one match in both tables.</p>'}]
            }
        ]
    }

    # 2. Data Science
    ds_data = {
        'title': 'Introduction to Data Science & AI',
        'description': 'Understand the basics of data analysis, visualization, and machine learning concepts.',
        'category': 'technical',
        'modules': [
            {
                'title': '1. Data Visualization',
                'lessons': [{'title': 'Matplotlib Basics', 'duration': 20, 'content': '<h3>Visualizing Data</h3><p>Learn how to create bar charts, line plots, and histograms.</p>'}]
            }
        ]
    }

    # 3. Cloud Basics
    cloud_data = {
        'title': 'Cloud Computing for Beginners',
        'description': 'Explore AWS, Azure, and Google Cloud basics. Understand scalability and deployment.',
        'category': 'technical',
        'modules': [
            {
                'title': '1. What is Cloud?',
                'lessons': [{'title': 'Introduction to IaaS/PaaS/SaaS', 'duration': 15, 'content': '<h3>Cloud Service Models</h3><p>Understand the difference between infrastructure, platform, and software as a service.</p>'}]
            }
        ]
    }

    all_extra = [sql_data, ds_data, cloud_data]

    for data in all_extra:
        course, _ = Course.objects.update_or_create(
            title=data['title'],
            defaults={'description': data['description'], 'category': data['category']}
        )
        for i, m_data in enumerate(data['modules']):
            module, _ = Module.objects.update_or_create(
                course=course, title=m_data['title'], defaults={'order': i + 1}
            )
            for j, l_data in enumerate(m_data['lessons']):
                Lesson.objects.update_or_create(
                    module=module, title=l_data['title'],
                    defaults={'content': l_data['content'], 'duration_minutes': l_data['duration'], 'order': j + 1}
                )
    
    print("Additional Courses Seeded.")

    # 2. Seed Notifications for ALL Candidates
    candidates = User.objects.filter(role='candidate')
    print(f"Seeding Notifications for {candidates.count()} candidates...")
    
    for c in candidates:
        Notification.objects.get_or_create(
            recipient=c,
            title='Welcome to TalentFlow AI!',
            defaults={
                'message': 'We are glad to have you. Explore the Learning Center to improve your skills and check your dashboard for interview schedules.',
                'notification_type': 'general',
                'is_read': False
            }
        )
        Notification.objects.get_or_create(
            recipient=c,
            title='Interview Scheduled: Senior Developer',
            defaults={
                'message': 'Your technical interview is scheduled for next Monday at 10:00 AM. Please check details in your dashboard.',
                'notification_type': 'interview_scheduled',
                'is_read': False
            }
        )
    
    print("All Notifications Seeded.")

if __name__ == '__main__':
    finalize_all_data()
