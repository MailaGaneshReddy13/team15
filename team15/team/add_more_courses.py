import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Module, Lesson

def add_more_courses():
    print("Adding 5 New LMS Courses...")

    # 1. Cyber Security
    cyber_data = {
        'title': 'Cyber Security Fundamentals',
        'description': 'Learn how to protect systems, networks, and programs from digital attacks.',
        'category': 'technical',
        'modules': [
            {'title': '1. Threat Landscape', 'lessons': [{'title': 'Common Attacks', 'duration': 15, 'content': '<h3>Phishing & Malware</h3><p>Understanding the most common vectors.</p>'}]}
        ]
    }

    # 2. DevOps
    devops_data = {
        'title': 'DevOps & CI/CD Pipelines',
        'description': 'Bridge the gap between development and operations with Docker, Kubernetes, and Jenkins.',
        'category': 'technical',
        'modules': [
            {'title': '1. Containerization', 'lessons': [{'title': 'Docker Basics', 'duration': 25, 'content': '<h3>Containers vs VMs</h3><p>Lightweight isolation for applications.</p>'}]}
        ]
    }

    # 3. Digital Marketing
    marketing_data = {
        'title': 'Digital Marketing 101',
        'description': 'Master SEO, Content Marketing, and Social Media strategies to grow a brand.',
        'category': 'career_prep',
        'modules': [
            {'title': '1. SEO Basics', 'lessons': [{'title': 'Keywords & Ranking', 'duration': 20, 'content': '<h3>Search Engine Optimization</h3><p>How to rank higher on Google.</p>'}]}
        ]
    }

    # 4. Blockchain
    blockchain_data = {
        'title': 'Blockchain & Web3 Fundamentals',
        'description': 'Understand the decentralized web, smart contracts, and cryptocurrency.',
        'category': 'technical',
        'modules': [
            {'title': '1. Distributed Ledger', 'lessons': [{'title': 'How Proof of Work Works', 'duration': 30, 'content': '<h3>Consensus Mechanisms</h3><p>The math behind Bitcoin and Ethereum.</p>'}]}
        ]
    }

    # 5. Mobile Dev
    mobile_data = {
        'title': 'Mobile App Development (Flutter)',
        'description': 'Build native mobile apps for iOS and Android using a single codebase.',
        'category': 'technical',
        'modules': [
            {'title': '1. Flutter Widgets', 'lessons': [{'title': 'Stateless vs Stateful', 'duration': 20, 'content': '<h3>Widget Tree</h3><p>Everything in Flutter is a widget.</p>'}]}
        ]
    }

    new_courses = [cyber_data, devops_data, marketing_data, blockchain_data, mobile_data]

    for data in new_courses:
        course, created = Course.objects.get_or_create(
            title=data['title'],
            defaults={'description': data['description'], 'category': data['category']}
        )
        if created:
            print(f"Created Course: {course.title}")
        else:
            print(f"Updated Course: {course.title}")

        for i, m_data in enumerate(data['modules']):
            module, _ = Module.objects.get_or_create(
                course=course, title=m_data['title'], defaults={'order': i + 1}
            )
            for j, l_data in enumerate(m_data['lessons']):
                Lesson.objects.get_or_create(
                    module=module, title=l_data['title'],
                    defaults={'content': l_data['content'], 'duration_minutes': l_data['duration'], 'order': j + 1}
                )
    
    print("Successfully added new courses.")

if __name__ == '__main__':
    add_more_courses()
