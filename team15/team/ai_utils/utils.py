import os
import json
from google import genai
from google.genai import types
from django.conf import settings

def get_gemini_client():
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or api_key == 'your_gemini_api_key_here':
        return None
    return genai.Client(api_key=api_key)

def parse_resume(file_text):
    mock_data = {
        "Name": "Sample Candidate",
        "Email": "candidate@example.com",
        "Phone": "123-456-7890",
        "Skills": ["Python", "Django", "SQL", "HTML", "CSS"],
        "Experience": "3 years of web development",
        "Education": "B.S. Computer Science"
    }
    
    if getattr(settings, 'GEMINI_MOCK_MODE', False):
        return mock_data
        
    client = get_gemini_client()
    if not client:
        return mock_data
        
    try:
        prompt = f"""
        Extract the following information from the resume text provided below in JSON format:
        - Name
        - Email
        - Phone
        - Skills (as a list)
        - Experience (summary)
        - Education (summary)

        Resume Text:
        {file_text}
        """
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"AI API Error (parse_resume): {e}")
        return mock_data

def analyze_match(resume_data, job_description):
    import random
    mock_data = {
        "match_score": random.randint(70, 95),
        "skills_matched": (resume_data.get('Skills', []) if resume_data else [])[:3],
        "missing_skills": ["Docker", "Kubernetes", "Cloud Deployment"],
        "ai_feedback": "The candidate shows a strong foundation in the core technologies required for this role, specifically Python and Django. However, their experience with cloud deployment and containerization tools like Docker seems limited compared to the job requirements. To become a top-tier candidate, they should focus on demonstrating practical experience with these missing skills in a production environment.",
        "improvement_suggestions": "Dimensions to improve: 1. Master Docker and Kubernetes for containerization. 2. Obtain an AWS Certified Developer associate certification. 3. Contribute to open-source projects involving microservices architecture."
    }

    if getattr(settings, 'GEMINI_MOCK_MODE', False):
        return mock_data
        
    client = get_gemini_client()
    if not client:
        return mock_data
        
    try:
        prompt = f"""
        Compare the following resume data with the job description.
        Resume: {json.dumps(resume_data)}
        Job Description: {job_description}

        Provide the following in JSON format:
        - match_score (0-100)
        - skills_matched (list)
        - missing_skills (list)
        - ai_feedback (string): A detailed analysis of the candidate's fit for the role. MUST be at least 3-4 sentences long, explaining why they are a good or bad match.
        - improvement_suggestions (string): Specific, actionable advice on what certifications, technologies, or projects the candidate should pursue to improve their chances.
        """
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"AI API Error (analyze_match): {e}")
        return mock_data

def generate_interview_questions(resume_data, job_title):
    # Mock Questions (30 total)
    mock_questions = []
    for i in range(10):
        mock_questions.append(f"Aptitude Q{i+1}: Logical reasoning question regarding data interpretation.")
    for i in range(10):
        mock_questions.append(f"Technical Q{i+1}: What is your experience with specific technology related to {job_title}?")
    for i in range(10):
        mock_questions.append(f"Behavioral Q{i+1}: Describe a situation where you had to solve a team conflict.")
    
    if getattr(settings, 'GEMINI_MOCK_MODE', False):
        return mock_questions
        
    client = get_gemini_client()
    if not client:
        return mock_questions
        
    retries = 3
    for attempt in range(retries):
        try:
            prompt = f"""
            Generate exactly 30 interview questions for a {job_title} role based on the candidate's resume.
            The questions MUST be split as follows:
            1. 10 Logical Reasoning questions compatible with a professional workplace (NO riddles like 'bat and ball', focus on data interpretation, pattern recognition, or work-place logic).
            2. 10 Technical questions tailored to the job and resume skills.
            3. 10 Non-technical/Behavioral questions.
            
            Resume: {json.dumps(resume_data)}
            
            Provide the response as a JSON list of strings [q1, q2, ..., q30].
            """
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            questions = json.loads(response.text)
            # Ensure we have 30
            if len(questions) < 30:
                questions.extend(mock_questions[len(questions):])
            return questions[:30]
        except Exception as e:
            print(f"AI API Error (generate_interview_questions) Attempt {attempt+1}: {e}")
            if attempt < retries - 1:
                import time
                # Aggressive backoff for 429 quota limits (30s, 60s, 120s)
                sleep_time = 30 * (2 ** attempt) 
                print(f"Waiting {sleep_time}s before retry (Attempt {attempt+1})...")
                time.sleep(sleep_time)
            else:
                return mock_questions

def evaluate_answer(question, answer):
    import random
    mock_eval = {
        "score": random.randint(7, 9),
        "feedback": "Excellent response. You showed deep technical knowledge.",
        "strengths": "Clear explanation, good use of terminology.",
        "improvements": "Could be more concise in the middle section."
    }
    
    if getattr(settings, 'GEMINI_MOCK_MODE', False):
        return mock_eval
        
    client = get_gemini_client()
    if not client:
        return mock_eval
        
    try:
        prompt = f"""
        Evaluate the following interview answer for the given question.
        Question: {question}
        Answer: {answer}

        Provide the following in JSON format:
        - score (0-10)
        - feedback (string)
        - strengths (string)
        - improvements (string)
        """
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"AI API Error (evaluate_answer): {e}")
        return mock_eval

def generate_quiz_questions(topic, resume_data=None):
    import random
    
    # Mock data for fallback testing - more specific than before
    mock_questions = []
    for i in range(30):
        mock_questions.append({
            "question": f"Question {i+1}: What is a core concept related to {topic} that every professional should know?",
            "options": [f"Concept A for {topic}", f"Concept B for {topic}", f"Concept C for {topic}", f"Concept D for {topic}"],
            "correct_answer": f"Concept A for {topic}"
        })

    if getattr(settings, 'GEMINI_MOCK_MODE', False) and not getattr(settings, 'GEMINI_API_KEY', None):
        return mock_questions
        
    client = get_gemini_client()
    if not client:
        return mock_questions
        
    try:
        context_str = ""
        if resume_data:
            context_str = f"Candidate Resume Context: {json.dumps(resume_data)}"

        prompt = f'''
        Generate 30 multiple-choice questions (MCQs) on the topic: "{topic}".
        {context_str}
        
        Requirements:
        1. Each question should have 4 options and 1 correct answer.
        2. The level should be intermediate/advanced, tailored to a candidate with the provided resume context if available.
        3. If resume context is provided, ensure questions touch upon technical skills or experience levels mentioned.
        
        Provide the output strictly as a JSON list of objects:
        [
            {{
                "question": "Question text here",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A"
            }},
            ...
        ]
        '''
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Robust parsing to handle potential markdown wrappers or conversational text
        text = response.text.strip()
        
        # Try to find the JSON array start
        start_idx = text.find('[')
        end_idx = text.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_text = text[start_idx:end_idx+1]
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                # If that fails, try the original backtick stripping
                if text.startswith('```'):
                    text = text.split('```')[1]
                    if text.startswith('json'):
                        text = text[4:]
                return json.loads(text)
        
        return json.loads(text)
    except Exception as e:
        print(f"AI API Error (generate_quiz_questions): {e}")
        print(f"Raw Response Content: {response.text if 'response' in locals() else 'No response'}")
        return mock_questions

def get_next_ai_question(session, candidate_response):
    """
    Uses Gemini to generate the next interviewer question or follow-up.
    """
    mock_response = "I see. Based on your background, can you describe a challenging technical problem you solved recently?"
    
    if getattr(settings, 'GEMINI_MOCK_MODE', False) and not getattr(settings, 'GEMINI_API_KEY', None):
        return mock_response
        
    client = get_gemini_client()
    if not client:
        return mock_response
        
    try:
        # Construct a more forceful context to prevent repetition
        prompt = f"""
        You are an expert AI Interviewer for a {session.role} position ({session.experience_level} level).
        Tech Stack: {session.tech_stack}.
        
        Session Progress: {session.transcript.count('AI:')} / {session.num_questions} questions asked.
        
        Recent Transcript:
        {session.transcript}
        
        Candidate's Response: "{candidate_response}"
        
        Task:
        1. Acknowledge the response briefly.
        2. Ask a NEW, distinct question related to the role and tech stack.
        3. DO NOT repeat questions already in the transcript.
        4. If {session.num_questions} questions have been asked, say: "Thank you for your time. The interview is now complete."
        5. Provide only the text for the interviewer to speak.
        """
        
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI API Error (get_next_ai_question): {e}")
        # Return a slightly different fallback to avoid extreme repetition
        if "Can you tell me more" in session.transcript:
            return "Moving on, how do you handle tight deadlines and technical debt?"
        return mock_response

def generate_detailed_feedback(transcript, role):
    """
    Analyzes an interview transcript using Gemini to provide structured feedback.
    """
    mock_feedback = {
        "communication_score": 85,
        "technical_score": 80,
        "problem_solving_score": 75,
        "cultural_fit_score": 90,
        "confidence_score": 85,
        "clarity_score": 80,
        "overall_score": 82.5,
        "feedback_summary": "The candidate demonstrated strong communication skills and a good understanding of core concepts. Technical depth could be improved in some areas.",
        "detailed_feedback": {
            "Communication": "Clear and concise delivery.",
            "Technical Knowledge": "Solid grasp of {role} fundamentals.",
            "Problem Solving": "Structured approach to challenges.",
            "Cultural Fit": "Values align well with standard professional environments.",
            "Confidence": "Articulated thoughts with poise.",
            "Clarity": "Explained complex ideas efficiently."
        }
    }

    if getattr(settings, 'GEMINI_MOCK_MODE', False):
        return mock_feedback
        
    client = get_gemini_client()
    if not client:
        return mock_feedback
        
    try:
        prompt = f"""
        Analyze the following interview transcript for a {role} position.
        
        Transcript:
        {transcript}
        
        Provide a detailed evaluation in JSON format with the following structure:
        {{
            "communication_score": (0-100),
            "technical_score": (0-100),
            "problem_solving_score": (0-100),
            "cultural_fit_score": (0-100),
            "confidence_score": (0-100),
            "clarity_score": (0-100),
            "overall_score": (0-100),
            "feedback_summary": "Short 2-3 sentence summary",
            "detailed_feedback": {{
                "Communication": "...",
                "Technical Knowledge": "...",
                "Problem Solving": "...",
                "Cultural Fit": "...",
                "Confidence": "...",
                "Clarity": "..."
            }}
        }}
        """
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"AI API Error (generate_detailed_feedback): {e}")
        return mock_feedback

