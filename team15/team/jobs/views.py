from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Resume, Application
from .forms import JobPostForm, ResumeUploadForm
from django.contrib import messages
from ai_utils.utils import parse_resume, analyze_match, get_gemini_client
import PyPDF2
import docx
import io
import json

def extract_skills_list(skills_text):
    """Helper to extract list of skills from comma-separated string."""
    if not skills_text:
        return []
    
    # Pre-clean strings from common template artifacts
    def clean_skill(s):
        if not isinstance(s, str):
            return str(s)
        # Remove literal {{ skill }} patterns and variations
        s = s.replace('{{', '').replace('}}', '').replace('{', '').replace('}', '').strip()
        return s

    if isinstance(skills_text, list):
        skills = [clean_skill(s) for s in skills_text]
        return [s for s in skills if s.lower() not in ['skills', 'skill', '']]
    
    # Remove "Skills:" prefix if present
    if ':' in skills_text:
        skills_text = skills_text.split(':', 1)[1]
        
    skills = [clean_skill(s) for s in skills_text.split(',') if s.strip()]
    return [s for s in skills if s.lower() not in ['skills', 'skill', '']]

def calculate_skills_match(resume_skills, job_skills_text):
    """
    Calculates matched and missing skills dynamically.
    resume_skills: list of strings
    job_skills_text: comma-separated string
    """
    # Normalize job skills (lowercase for comparison)
    job_skills_list = extract_skills_list(job_skills_text)
    job_skills_set = set(s.lower() for s in job_skills_list)
    
    # Normalize resume skills
    if isinstance(resume_skills, str):
        # Handle case where resume_skills might be a string
        resume_skills = extract_skills_list(resume_skills)
    
    resume_skills_set = set(s.lower() for s in resume_skills)

    # Calculate matches (intersection)
    # We want to return the original formatting from Job/Resume if possible, or just the lowercase keys
    # For display, let's try to preserve title casing from Job requirements if it matches
    
    matched_skills_lower = job_skills_set.intersection(resume_skills_set)
    missing_skills_lower = job_skills_set.difference(resume_skills_set)
    
    # Re-map to original cases for display niceness
    matched_skills = []
    missing_skills = []
    
    # Map back to original job skill casing
    for skill in job_skills_list:
        if skill.lower() in matched_skills_lower:
            matched_skills.append(skill)
        elif skill.lower() in missing_skills_lower:
            missing_skills.append(skill)
            
    # Paranoid verification check
    # Ensure no template placeholders slipped through
    final_missing = []
    for skill in missing_skills:
        clean = skill.replace('{', '').replace('}', '').strip()
        if clean.lower() not in ['skill', 'skills', '']:
            final_missing.append(skill)
            
    return matched_skills, final_missing
    
def get_recommended_courses(missing_skills):
    """Helper to get recommended courses based on missing skills."""
    from lms.models import Course
    from django.db.models import Q
    
    search_terms = missing_skills
    query = Q()
    for term in search_terms:
        # Search title and description for each skill
        query |= Q(title__icontains=term) | Q(description__icontains=term)
        
    recommended_courses = []
    if query:
        # Get ALL matching courses, no limit
        recommended_courses = list(Course.objects.filter(query).distinct())
        
    return recommended_courses

@login_required
def post_job(request):
    if request.user.role != 'hr':
        return redirect('dashboard')
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.hr = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('hr_jobs')
    else:
        form = JobPostForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    # Security check: only the HR user who posted the job can edit it
    if request.user.role != 'hr' or job.hr != request.user:
        messages.error(request, "You do not have permission to edit this job.")
        return redirect('hr_jobs')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('hr_jobs')
    else:
        form = JobPostForm(instance=job)
    
    return render(request, 'jobs/post_job.html', {
        'form': form,
        'is_edit': True,
        'job': job
    })

@login_required
def hr_jobs(request):
    if request.user.role != 'hr':
        return redirect('dashboard')
    jobs = request.user.posted_jobs.all()
    return render(request, 'jobs/hr_jobs.html', {'jobs': jobs})

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(skills_required__icontains=query)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resume_obj = form.save(commit=False)
                resume_obj.candidate = request.user
                resume_obj.save()
                
                # Extract text
                file_text = ""
                file = request.FILES['file']
                try:
                    file.seek(0)
                    if file.name.endswith('.pdf'):
                        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                        for page in reader.pages:
                            file_text += page.extract_text()
                    elif file.name.endswith('.docx'):
                        doc = docx.Document(file)
                        for para in doc.paragraphs:
                            file_text += para.text + "\n"
                    else:
                        # Fallback for other text files
                        file_text = file.read().decode('utf-8', errors='ignore')

                except Exception as e:
                    messages.error(request, f"Extraction Error: {e}")
                    return redirect('apply_job', pk=pk)
                
                # 1. AI Parse - Extract Skills
                parsed_data = parse_resume(file_text)
                resume_obj.parsed_data = parsed_data
                resume_obj.save()
                
                # 2. Extract Job Skills
                job_skills_text = job.skills_required
                
                # 3. Dynamic Matching
                resume_skills = parsed_data.get('Skills', [])
                matched_skills, missing_skills = calculate_skills_match(resume_skills, job_skills_text)
                
                # AI Match - Get Score & Feedback Only
                # We still use AI for score and feedback, but we override the skills lists
                # PASS MISSING SKILLS TO AI FOR BETTER SUGGESTIONS
                match_data = analyze_match(parsed_data, job.description, missing_skills)
                
                # Update resume with calculated data
                resume_obj.match_score = match_data.get('match_score', 0)
                resume_obj.ai_feedback = match_data.get('ai_feedback', '')
                
                # Store as comma-separated string for DB compatibility, but views will recalculate lists
                resume_obj.skills_matched = ", ".join(matched_skills)
                resume_obj.missing_skills = ", ".join(missing_skills)
                resume_obj.improvement_suggestions = match_data.get('improvement_suggestions', '')
                resume_obj.save()
                
                return redirect('screening_preview', resume_id=resume_obj.id, job_id=job.id)
            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f"Screening Error: {e}")
                return redirect('apply_job', pk=pk)
    else:
        form = ResumeUploadForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def screening_preview(request, resume_id, job_id):
    resume = get_object_or_404(Resume, id=resume_id, candidate=request.user)
    job = get_object_or_404(Job, id=job_id)
    
    # Dynamic Recalculation (Fresh on every request)
    # print(f"DEBUG: Job ID {job.id}, Skills: {job.skills_required}")
    resume_skills = resume.parsed_data.get('Skills', [])
    # print(f"DEBUG: Resume Skills: {resume_skills}")
    matched_skills, missing_skills = calculate_skills_match(resume_skills, job.skills_required)
    # print(f"DEBUG: Calculated Missing Skills: {missing_skills}")

    # FORCE UPDATE AI ANALYSIS (to fix stale data for the user)
    import datetime
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Re-run analysis with fresh prompt requirements
    match_data = analyze_match(resume.parsed_data, job.description, missing_skills)
    
    # Update AND Save the resume with clean feedback
    resume.match_score = match_data.get('match_score', 0)
    resume.ai_feedback = match_data.get('ai_feedback', '')
    resume.improvement_suggestions = match_data.get('improvement_suggestions', '')
    resume.save()

    # Recommender System (Matches ALL missing skills)
    recommended_courses = get_recommended_courses(missing_skills)

    context = {
        'resume': resume,
        'job': job,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'recommended_courses': recommended_courses,
        'last_updated': now_str
    }
    return render(request, 'jobs/screening_preview.html', context)

from lms.models import Course
from django.db.models import Q

@login_required
def confirm_apply(request, resume_id, job_id):
    resume = get_object_or_404(Resume, id=resume_id, candidate=request.user)
    job = get_object_or_404(Job, id=job_id)
    
    # Strict Gatekeeper Check
    status = 'applied'
    if resume.match_score < 80:
         status = 'rejected'
         messages.warning(request, "Your resume match score is below 80%. Your application has been flagged for review, and we recommend upskilling.")
    
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', pk=job.id)
        
    # Recalculate one last time
    resume_skills = resume.parsed_data.get('Skills', [])
    matched_skills, missing_skills = calculate_skills_match(resume_skills, job.skills_required)

    app = Application.objects.create(
        job=job,
        candidate=request.user,
        resume=resume,
        match_score=resume.match_score,
        ai_feedback=resume.ai_feedback,
        skills_matched=", ".join(matched_skills),
        missing_skills=", ".join(missing_skills),
        improvement_suggestions=resume.improvement_suggestions,
        status=status
    )
    
    if status == 'applied':
        messages.success(request, "Application submitted successfully!")
    
    return redirect('screening_result', pk=app.id)

@login_required
def screening_result(request, pk):
    application = get_object_or_404(Application, pk=pk, candidate=request.user)
    
    resume_skills = application.resume.parsed_data.get('Skills', []) if application.resume else []
    matched_skills, missing_skills = calculate_skills_match(resume_skills, application.job.skills_required)

    # Recommender System
    recommended_courses = []
    if application.match_score < 80:
        recommended_courses = get_recommended_courses(missing_skills)

    context = {
        'application': application,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'recommended_courses': recommended_courses
    }
    return render(request, 'jobs/screening_result.html', context)

@login_required
def view_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk, hr=request.user)
    applicants = job.applications.all().order_by('-match_score')
    return render(request, 'jobs/view_applicants.html', {'job': job, 'applicants': applicants})

@login_required
def update_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk, job__hr=request.user)
    if status in ['shortlisted', 'rejected', 'interview']:
        application.status = status
        application.save()
        messages.success(request, f"Status updated to {status.capitalize()}")
    return redirect('view_applicants', pk=application.job.id)

@login_required
def my_applications(request):
    apps = request.user.job_applications.all().order_by('-applied_at')
    return render(request, 'jobs/my_applications.html', {'applications': apps})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.user.role != 'hr' and application.candidate != request.user:
        return redirect('dashboard')
        
    # Dynamic Calculation
    resume_skills = application.resume.parsed_data.get('Skills', []) if application.resume else []
    matched_skills, missing_skills = calculate_skills_match(resume_skills, application.job.skills_required)

    candidate_name = application.candidate.get_full_name()
    candidate_name = application.candidate.get_full_name()
    if not candidate_name:
        candidate_name = application.candidate.username

    context = {
        'app': application,
        'candidate_name': candidate_name,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills
    }
    return render(request, 'jobs/application_detail.html', context)
