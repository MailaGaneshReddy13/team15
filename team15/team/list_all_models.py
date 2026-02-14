import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

def list_models():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("No API key found")
        return

    client = genai.Client(api_key=api_key)
    try:
        with open('models_list.txt', 'w', encoding='utf-8') as f:
            for m in client.models.list():
                f.write(m.name + '\n')
                print(m.name) # Also print to stdout
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
