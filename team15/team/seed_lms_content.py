import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Module, Lesson

def seed_more_courses():
    courses_data = [
        {
            "title": "Advanced System Architecture",
            "description": "Master the design of scalable, resilient, and high-performance distributed systems. Covers microservices, event-driven architecture, and CAP theorem.",
            "category": "technical",
            "modules": [
                {
                    "title": "Architectural Patterns",
                    "lessons": [
                        {"title": "Monolith vs Microservices", "content": "Learn the pros and cons of different architectural styles..."},
                        {"title": "Event Sourcing & CQRS", "content": "Understanding state changes in distributed systems..."}
                    ]
                }
            ]
        },
        {
            "title": "Agile Project Management",
            "description": "Deep dive into Scrum, Kanban, and Lean methodologies for engineering managers and team leads.",
            "category": "career_prep",
            "modules": [
                {
                    "title": "Scrum Framework",
                    "lessons": [
                        {"title": "Sprints and Standups", "content": "Mastering the daily rituals of high-performing teams..."},
                        {"title": "Backlog Grooming", "content": "Prioritizing value for the stakeholder..."}
                    ]
                }
            ]
        },
        {
            "title": "Conflict Resolution for Teams",
            "description": "Essential soft skills for navigating difficult conversations and building high-trust workplace cultures.",
            "category": "soft_skills",
            "modules": [
                {
                    "title": "Communication Strategies",
                    "lessons": [
                        {"title": "Active Listening", "content": "How to truly hear what your colleagues are saying..."},
                        {"title": "Giving Feedback", "content": "The art of non-violent communication in tech..."}
                    ]
                }
            ]
        },
        {
            "title": "Cloud Native Security",
            "description": "Secure your infrastructure using modern tools and practices. Zero trust, IAM, and container security.",
            "category": "technical",
            "modules": [
                {
                    "title": "Zero Trust Security",
                    "lessons": [
                        {"title": "Identity as a Perimeter", "content": "Moving away from traditional VPNs..."},
                        {"title": "Secrets Management", "content": "Handling keys and tokens securely..."}
                    ]
                }
            ]
        },
        {
            "title": "Docker and Kubernetes Deep Dive",
            "description": "Go from container basics to managing production-grade clusters with Kubernetes.",
            "category": "technical",
            "modules": [
                {
                    "title": "Kubernetes Orchestration",
                    "lessons": [
                        {"title": "Pods and Deployments", "content": "The building blocks of K8s..."},
                        {"title": "Services and Ingress", "content": "Routing traffic to your containers..."}
                    ]
                }
            ]
        }
    ]

    for c_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=c_data["title"],
            defaults={
                "description": c_data["description"],
                "category": c_data["category"],
                "requires_final_quiz": True
            }
        )
        if created:
            print(f"Added course: {course.title}")
            for m_idx, m_data in enumerate(c_data["modules"]):
                module = Module.objects.create(
                    course=course,
                    title=m_data["title"],
                    order=m_idx
                )
                for l_idx, l_data in enumerate(m_data["lessons"]):
                    Lesson.objects.create(
                        module=module,
                        title=l_data["title"],
                        content=l_data["content"],
                        order=l_idx
                    )
        else:
            print(f"Course already exists: {course.title}")

if __name__ == "__main__":
    seed_more_courses()
