from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InterviewSession, InterviewQuestion, InterviewAnswer, LiveInterview, AIInterviewSession, Notification
from jobs.models import Application, Job
from ai_utils.utils import (
    generate_interview_questions, 
    evaluate_answer, 
    get_next_ai_question, 
    generate_detailed_feedback
)
from django.http import JsonResponse
import json
import uuid
from django.contrib import messages

@login_required
def start_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id, candidate=request.user)
    
    # Create or get existing session
    session, created = InterviewSession.objects.get_or_create(
        candidate=request.user,
        job=application.job,
        is_completed=False
    )
    
    if created or session.questions.count() == 0:
        # Generate questions using AI only for brand-new sessions
        if not created:
             session.questions.all().delete()
             
        resume_data = application.resume.parsed_data
        questions_list = generate_interview_questions(resume_data, application.job.title)
        
        for i, q_text in enumerate(questions_list):
            InterviewQuestion.objects.create(
                session=session,
                text=q_text,
                order=i+1
            )
            
    return render(request, 'interviews/interview.html', {'session': session})

@login_required
def get_question(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)
    # Find next unanswered question
    unanswered = session.questions.filter(answer__isnull=True).order_by('order').first()
    
    if unanswered:
        return JsonResponse({
            'id': unanswered.id,
            'text': unanswered.text,
            'order': unanswered.order,
            'total': session.questions.count(),
            'finished': False
        })
    else:
        # Evaluate session if all questions answered
        if not session.is_completed:
            evaluate_session(session)
        return JsonResponse({'finished': True})

def evaluate_session(session):
    answers = InterviewAnswer.objects.filter(question__session=session)
    if not answers:
        return
    
    total_score = sum(a.score for a in answers)
    total_questions = session.questions.count()
    if total_questions == 0:
        avg_score = 0
    else:
        avg_score = (total_score / (total_questions * 10)) * 100
    
    session.overall_score = avg_score
    session.is_completed = True
    session.save()
    
    # Update application status
    app = Application.objects.filter(job=session.job, candidate=session.candidate).first()
    if app:
        app.status = 'interview' # Keep as interview but completed
        app.save()

@login_required
def submit_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer_text = data.get('answer')
        
        question = get_object_or_404(InterviewQuestion, id=question_id, session__candidate=request.user)
        
        # AI evaluate answer
        evaluation = evaluate_answer(question.text, answer_text)
        
        InterviewAnswer.objects.create(
            question=question,
            answer_text=answer_text,
            score=evaluation.get('score', 0),
            feedback=evaluation.get('feedback', ''),
            strengths=evaluation.get('strengths', ''),
            improvements=evaluation.get('improvements', '')
        )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def interview_report(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)
    if not session.is_completed:
        return redirect('mock_interview', application_id=Application.objects.get(job=session.job, candidate=session.candidate).id)
    
    questions = session.questions.all().order_by('order')
    return render(request, 'interviews/report.html', {'session': session, 'questions': questions})

@login_required
def finish_interview(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)
    evaluate_session(session)
    return redirect('interview_report', session_id=session.id)

@login_required
def schedule_live_interview(request, application_id):
    if request.user.role != 'hr':
        messages.error(request, "Only HR can schedule interviews.")
        return redirect('dashboard')
        
    application = get_object_or_404(Application, id=application_id)
    
    # Verify HR owns the job
    if application.job.hr != request.user:
         messages.error(request, "You are not authorized to view this application.")
         return redirect('hr_jobs')

    if request.method == 'POST':
        scheduled_at = request.POST.get('scheduled_at')
        duration = request.POST.get('duration', 30)
        
        # Generate a unique meeting ID
        meeting_id = f"{application.id}-{uuid.uuid4().hex[:8]}"
        
        live_interview = LiveInterview.objects.create(
            application=application,
            interviewer=request.user,
            scheduled_at=scheduled_at,
            meeting_id=meeting_id,
            duration_minutes=duration
        )
        
        # Create notification for the candidate
        from django.utils.dateparse import parse_datetime
        scheduled_dt = parse_datetime(scheduled_at)
        time_str = scheduled_dt.strftime('%B %d, %Y at %I:%M %p') if scheduled_dt else scheduled_at
        Notification.objects.create(
            recipient=application.candidate,
            title=f"Interview Scheduled: {application.job.title}",
            message=f"Your interview for the '{application.job.title}' position has been scheduled on {time_str}. Duration: {duration} minutes. Meeting ID: {meeting_id}. Please be prepared and join on time.",
            notification_type='interview_scheduled',
            related_interview=live_interview
        )
        
        messages.success(request, f"Live interview scheduled for {application.candidate.username}.")
        return redirect('application_detail', pk=application.id)
        
    return render(request, 'interviews/live_schedule.html', {'application': application})

@login_required
def live_interview_room(request, meeting_id):
    interview = get_object_or_404(LiveInterview, meeting_id=meeting_id)
    
    # Check permissions
    if request.user != interview.interviewer and request.user != interview.application.candidate:
        messages.error(request, "You are not authorized to join this interview.")
        return redirect('dashboard')
        
    context = {
        'interview': interview,
        'is_hr': request.user.role == 'hr',
        'jitsi_domain': "meet.jit.si",
        'room_name': f"TalentFlow-Interview-{meeting_id}",
    }
    return render(request, 'interviews/live_room.html', context)

@login_required
def ai_interview_setup(request):
    """
    Setup page for personalized AI interview (Voice Input).
    """
    return render(request, 'interviews/ai_interview_setup.html')

@login_required
def start_ai_interview(request):
    """
    Endpoint to initialize the AI interview session.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = data.get('role', 'Software Engineer')
            exp = data.get('experience_level', 'Junior')
            type_ = data.get('interview_type', 'Technical')
            stack = data.get('tech_stack', 'General')
            import re
            num_q_raw = str(data.get('num_questions', '5'))
            # Find the first sequence of digits
            match = re.search(r'\d+', num_q_raw)
            if match:
                num_q = int(match.group())
            else:
                # Fallback mapping for common word numbers if no digits found
                word_map = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 
                           'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
                num_q = word_map.get(num_q_raw.lower().strip('. '), 5)
            
            # Create Session
            session = AIInterviewSession.objects.create(
                candidate=request.user,
                role=role,
                experience_level=exp,
                interview_type=type_,
                tech_stack=stack,
                num_questions=num_q,
                transcript=""
            )
            
            # Generate the first question
            first_question = get_next_ai_question(session, "Hello, I am ready to start.")
            session.transcript += f"AI: {first_question}\n"
            session.save()
            
            return JsonResponse({
                'status': 'success',
                'session_id': session.id,
                'first_question': first_question
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

@login_required
def chat_with_interviewer(request, session_id):
    """
    Endpoint for dynamic voice-based conversation.
    """
    session = get_object_or_404(AIInterviewSession, id=session_id, candidate=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        candidate_response = data.get('response', '')
        current_code = data.get('code', '')
        
        # Append candidate response to transcript
        session.transcript += f"Candidate: {candidate_response}\n"
        if current_code and current_code != "# Write your code here...":
             # We can optionally tag the code here or just pass it to the AI
             pass
        
        # Get next question from Gemini, now with code awareness
        next_question = get_next_ai_question(session, candidate_response, current_code)
        
        # Append AI question to transcript
        session.transcript += f"AI: {next_question}\n"
        session.save()
        
        return JsonResponse({
            'status': 'success',
            'next_question': next_question,
            'is_finished': "interview is complete" in next_question.lower() or "thank you" in next_question.lower()
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def ai_interview_room(request, session_id):
    """
    The interactive interview room where Vapi SDK is used.
    """
    session = get_object_or_404(AIInterviewSession, id=session_id, candidate=request.user)
    return render(request, 'interviews/ai_interview_room.html', {'session': session})

@login_required
def process_ai_feedback(request, session_id):
    """
    Endpoint to trigger Gemini feedback once the interview is finished.
    """
    session = get_object_or_404(AIInterviewSession, id=session_id, candidate=request.user)
    if not session.transcript:
        return JsonResponse({'status': 'error', 'message': 'No transcript found'}, status=400)
        
    # Generate detailed feedback using Gemini
    feedback = generate_detailed_feedback(session.transcript, session.role)
    
    session.communication_score = feedback.get('communication_score', 0)
    session.technical_score = feedback.get('technical_score', 0)
    session.problem_solving_score = feedback.get('problem_solving_score', 0)
    session.cultural_fit_score = feedback.get('cultural_fit_score', 0)
    session.confidence_score = feedback.get('confidence_score', 0)
    session.clarity_score = feedback.get('clarity_score', 0)
    session.overall_score = feedback.get('overall_score', 0)
    session.feedback_summary = feedback.get('feedback_summary', '')
    session.detailed_feedback = feedback.get('detailed_feedback', {})
    
    session.is_completed = True
    session.save()
    
    return JsonResponse({'status': 'success', 'redirect_url': f'/interviews/ai-report/{session.id}/'})

@login_required
def ai_interview_report(request, session_id):
    """
    Report page for the AI interview session.
    """
    session = get_object_or_404(AIInterviewSession, id=session_id, candidate=request.user)
    if not session.is_completed:
        return redirect('ai_interview_room', session_id=session.id)
    
    # Prepare data for Chart.js
    radar_data = {
        'Communication': session.communication_score,
        'Technical Knowledge': session.technical_score,
        'Problem Solving': session.problem_solving_score,
        'Cultural Fit': session.cultural_fit_score,
        'Confidence': session.confidence_score,
        'Clarity': session.clarity_score,
    }
    
    return render(request, 'interviews/ai_report.html', {
        'session': session,
        'radar_data_json': json.dumps(radar_data)
    })

@login_required
def delete_interview_session(request, session_id):
    """
    Delete a mock interview session. Only available for the candidate.
    """
    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)
    if request.method == 'POST':
        app = Application.objects.filter(job=session.job, candidate=request.user).first()
        application_id = app.id if app else None
        session.delete()
        messages.success(request, "Interview history deleted successfully.")
        if application_id:
            return redirect('application_detail', pk=application_id)
        return redirect('dashboard')
    return redirect('interview_report', session_id=session.id)

@login_required
def delete_ai_interview_session(request, session_id):
    """
    Delete an AI interview session. Only available for the candidate.
    """
    session = get_object_or_404(AIInterviewSession, id=session_id, candidate=request.user)
    if request.method == 'POST':
        session.delete()
        messages.success(request, "AI Interview session deleted successfully.")
        return redirect('dashboard')
    return redirect('ai_interview_report', session_id=session.id)

@login_required
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
    return redirect('dashboard')
