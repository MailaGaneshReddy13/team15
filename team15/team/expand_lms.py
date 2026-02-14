import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Module, Lesson

def expand_lms_categories():
    print("Expanding LMS Categories...")

    # Logic & Aptitude
    logic_data = {
        'title': 'Logic & Logical Reasoning',
        'description': 'Sharpen your analytical skills with logical reasoning, pattern recognition, and workplace logic.',
        'category': 'career_prep',
        'modules': [
            {'title': '1. Deductive Reasoning', 'lessons': [{'title': 'Introduction to Logic', 'duration': 20, 'content': '<h3>Basic Logic</h3><p>Learn how to identify premises and conclusions.</p>'}]}
        ]
    }

    # Project Management
    pm_data = {
        'title': 'Modern Project Management (Agile/Scrum)',
        'description': 'Learn how to manage software projects using Agile methodologies, Scrum, and Kanban.',
        'category': 'soft_skills',
        'modules': [
            {'title': '1. Agile Principles', 'lessons': [{'title': 'The Agile Manifesto', 'duration': 15, 'content': '<h3>Agile Basics</h3><p>Focus on individuals and interactions over processes and tools.</p>'}]}
        ]
    }

    # System Design
    sd_data = {
        'title': 'System Design & Scalability',
        'description': 'Advanced course for architects and developers. Learn how to build large-scale distributed systems.',
        'category': 'technical',
        'modules': [
            {'title': '1. Load Balancing', 'lessons': [{'title': 'Horizontal vs Vertical Scaling', 'duration': 30, 'content': '<h3>Scaling</h3><p>Learn when to add more servers vs more power.</p>'}]}
        ]
    }

    all_data = [logic_data, pm_data, sd_data]

    for data in all_data:
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
    
    print("New Categories Added.")

if __name__ == '__main__':
    expand_lms_categories()
