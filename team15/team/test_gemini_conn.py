import os
import django
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from ai_utils.utils import get_gemini_client

def test_gemini():
    client = get_gemini_client()
    if not client:
        print("Failed to get Gemini client.")
        return

    try:
        print("Listing available models...")
        for model in client.models.list():
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    test_gemini()
