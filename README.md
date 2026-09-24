# HR Resume Screener and Interview Agent

## 📌 Project Overview

The **HR Resume Screener and Interview Agent** is an AI-powered recruitment system designed to automate the initial stages of the hiring process. It analyzes candidate resumes against job requirements, calculates a matching score, and conducts an AI-based interview to help HR teams shortlist suitable candidates.

The system reduces manual resume screening, saves time, and provides a structured approach to candidate evaluation.

## 🎯 Objectives

* Automate resume screening and candidate shortlisting.
* Match candidate skills with job requirements.
* Generate a resume matching score.
* Conduct AI-based mock interviews.
* Evaluate candidate answers automatically.
* Provide interview scores and recruitment reports.
* Help HR managers manage jobs and candidates efficiently.

## 🚀 Key Features

### 1. User Authentication

* HR/Admin registration and login.
* Candidate registration and login.
* Secure access based on user roles.

### 2. Job Management

HR can:

* Create job postings.
* Add job descriptions.
* Specify required skills.
* Add salary and other job details.
* Manage available job positions.

### 3. Resume Upload

Candidates can upload their resumes in supported formats.

### 4. Resume Parsing

The system extracts important information such as:

* Skills
* Education
* Experience
* Certifications
* Projects

### 5. AI Resume Matching

The system compares the candidate's resume with the selected job description using NLP and matching techniques.

**Matching Score:** 0–100%

Candidates meeting the configured threshold can proceed to the interview stage.

### 6. AI Interview Agent

The AI Interview Agent:

* Generates relevant interview questions.
* Interacts with candidates through a chatbot interface.
* Evaluates candidate responses.
* Generates an interview score.

### 7. Candidate Shortlisting

HR can view candidate details, resume scores, interview scores, and shortlist candidates based on the recruitment criteria.

### 8. Reports

The system can generate candidate evaluation information including:

* Resume matching score
* Interview score
* Skills
* Candidate details
* Final recruitment status

## 🔄 System Workflow

```text
HR Login/Register
       ↓
Post Job
       ↓
Candidate Login/Register
       ↓
Search & Select Job
       ↓
Upload Resume
       ↓
Resume Parsing
       ↓
AI Resume Matching
       ↓
Matching Score
       ↓
Candidate Shortlisting
       ↓
AI Interview
       ↓
Answer Evaluation
       ↓
Interview Score
       ↓
HR Review
       ↓
Final Selection / Rejection
```

## 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │   HR / Admin    │
                    └────────┬────────┘
                             │
                       Job Management
                             │
                             ▼
                    ┌─────────────────┐
                    │  HR Platform    │
                    └────────┬────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
      Resume Parser    AI Matching     Interview Agent
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                    ┌─────────────────┐
                    │    Database     │
                    └─────────────────┘
                             │
                             ▼
                    Candidate Reports
```

## 🧠 Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Django

### AI / Machine Learning

* Natural Language Processing (NLP)
* Resume Parsing
* Text Similarity
* AI-based Answer Evaluation

### Database

* SQLite / MySQL

### Tools

* Visual Studio Code
* Git
* GitHub

## 📂 Project Structure

```text
HR-Resume-Screener/
│
├── manage.py
├── requirements.txt
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── resume/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── interview/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── upload_resume.html
│   └── interview.html
│
├── static/
│   ├── css/
│   └── js/
│
└── media/
    └── resumes/
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hr-resume-screener.git
cd hr-resume-screener
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## 👥 User Roles

| Role          | Functions                                                         |
| ------------- | ----------------------------------------------------------------- |
| **HR/Admin**  | Create jobs, view candidates, review scores, shortlist candidates |
| **Candidate** | Register, search jobs, upload resume, attend AI interview         |

## 📊 Resume Matching

The resume matching module analyzes the relationship between:

```text
Job Description
       +
Candidate Resume
       ↓
Text Processing
       ↓
Skill Extraction
       ↓
Similarity Analysis
       ↓
Matching Score
```

The matching score is used as one input for determining whether a candidate proceeds to the interview stage.

## 🎤 AI Interview

The interview module provides:

* Technical questions
* HR questions
* Candidate response collection
* Automated answer evaluation
* Interview score
* Interview report

## 🔐 Security

The system is designed to support:

* User authentication
* Role-based access
* Secure resume uploads
* Candidate data protection
* Database access control

## 🔮 Future Scope

* Voice-based AI interviews.
* Video interview analysis.
* Multilingual interviews.
* Advanced semantic resume matching.
* Integration with job portals.
* Automated interview scheduling.
* Advanced HR analytics dashboard.
* Email notifications for candidates and HR.
* Integration with large language models.

## ✅ Advantages

* Reduces manual resume screening.
* Saves HR processing time.
* Provides consistent evaluation criteria.
* Automates the initial interview process.
* Makes candidate information easier to manage.
* Generates structured candidate evaluation data.

## 📝 Conclusion

The **HR Resume Screener and Interview Agent** provides an AI-assisted approach to recruitment by combining resume parsing, job matching, candidate shortlisting, and automated interviews. It helps streamline the initial hiring workflow and provides HR teams with structured information for candidate review.

