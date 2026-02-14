import os
import django
import sys
import json

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

def test_http_request():
    User = get_user_model()
    # Find a user with a resume
    from jobs.models import Resume
    
    target_user = None
    for user in User.objects.all():
        if Resume.objects.filter(candidate=user).exists():
            target_user = user
            break
            
    if not target_user:
        print("No user with resume found.")
        return

    print(f"Testing with user: {target_user.username}")
    
    client = Client()
    client.force_login(target_user)
    
    url = "/api/quiz/questions/?topic=Python"
    print(f"Requesting URL: {url}")
    
    try:
        response = client.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'questions' in data:
                print(f"Success! Received {len(data['questions'])} questions.")
            else:
                print(f"Response data: {data}")
        else:
            print(f"Error Response: {response.content.decode('utf-8')[:500]}")
            if b'<title>' in response.content:
                title = response.content.split(b'<title>')[1].split(b'</title>')[0]
                print(f"Page Title: {title.decode('utf-8')}")
            
    except Exception as e:
        print(f"Client Request Failed: {e}")

if __name__ == "__main__":
    test_http_request()
