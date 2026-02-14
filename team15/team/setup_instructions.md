# HR Resume Screener & AI Interview Agent - Setup Instructions

Follow these steps to get the project running locally:

## Prerequisites
- Python 3.8+
- Gemini API Key (get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. **Clone or Download** the project to your local machine.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   - Create a `.env` file (optional) or set your Gemini API key in `hr_agent/settings.py` or as an environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   *(On Windows use `set GEMINI_API_KEY="your-api-key-here"`)

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations accounts jobs interviews
   python manage.py migrate
   ```

5. **Create a Superuser** (Admin):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- **Home Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Registration**: Choose role "HR" to post jobs or "Candidate" to apply.
- **HR Dashboard**: Post jobs and view applicants with AI scores.
- **Candidate Dashboard**: Browse jobs, upload resumes, and take AI-driven mock interviews.

## Note on AI
The project uses the `gemini-2.0-flash` model for high-speed analysis. Ensure your API key has access to this model.
