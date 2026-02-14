from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import QuizAttempt
from ai_utils.utils import generate_quiz_questions

@login_required
def quiz_home(request):
    from jobs.models import Resume
    
    # Fetch the latest resume skills for suggestions
    latest_resume = Resume.objects.filter(candidate=request.user).order_by('-uploaded_at').first()
    suggested_skills = []
    if latest_resume and latest_resume.parsed_data:
        suggested_skills = latest_resume.parsed_data.get('Skills', [])
    
    # Accept a topic from GET parameters for auto-start
    preset_topic = request.GET.get('topic', '')
    
    context = {
        'suggested_skills': suggested_skills,
        'preset_topic': preset_topic
    }
    return render(request, 'quiz/home.html', context)

@login_required
def get_quiz_questions(request):
    topic = request.GET.get('topic')
    if not topic:
        return JsonResponse({'error': 'Topic is required'}, status=400)
    
    from jobs.models import Resume
    latest_resume = Resume.objects.filter(candidate=request.user).order_by('-uploaded_at').first()
    resume_data = latest_resume.parsed_data if latest_resume else None
    
    questions = generate_quiz_questions(topic, resume_data=resume_data)
    return JsonResponse({'questions': questions})

@login_required
@require_POST
def submit_quiz_result(request):
    try:
        data = json.loads(request.body)
        topic = data.get('topic')
        score = data.get('score')
        total = data.get('total', 30)
        
        if not topic or score is None:
            return JsonResponse({'error': 'Missing data'}, status=400)
            
        QuizAttempt.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total_questions=total
        )
        
        # LINK TO LMS PROGRESS: If this was a final course quiz
        from lms.models import UserCourseProgress
        # Find any active progress for a course that uses this topic for its final quiz
        progresses = UserCourseProgress.objects.filter(
            user=request.user, 
            course__final_quiz_topic__iexact=topic,
            final_quiz_passed=False
        )
        for p in progresses:
            if (score / total) >= 0.8:
                p.final_quiz_passed = True
                p.save()
                # Check for overall completion
                if p.progress_percent == 100 and not p.is_completed:
                    p.is_completed = True
                    p.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def quiz_history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-date')
    return render(request, 'quiz/history.html', {'attempts': attempts})
