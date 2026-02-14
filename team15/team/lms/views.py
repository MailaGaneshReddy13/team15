from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, UserCourseProgress
from django.contrib import messages

@login_required
def course_list(request):
    courses = Course.objects.all()
    user_progress = {}
    for progress in UserCourseProgress.objects.filter(user=request.user):
        user_progress[progress.course.id] = progress.progress_percent
        
    return render(request, 'lms/course_list.html', {
        'courses': courses,
        'user_progress': user_progress
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.prefetch_related('lessons').all()
    
    # Get or create progress
    progress, created = UserCourseProgress.objects.get_or_create(user=request.user, course=course)
    completed_lesson_ids = progress.completed_lessons.values_list('id', flat=True)
    
    return render(request, 'lms/course_detail.html', {
        'course': course,
        'modules': modules,
        'completed_lesson_ids': completed_lesson_ids,
        'progress': progress,
        'all_lessons_completed': progress.completed_lessons.count() == course.total_lessons
    })

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course
    
    # Update progress
    progress, created = UserCourseProgress.objects.get_or_create(user=request.user, course=course)
    if lesson not in progress.completed_lessons.all():
        progress.completed_lessons.add(lesson)
        progress.save()
        
    # Check if course is completed
    is_now_completed = False
    if progress.progress_percent == 100 and not progress.is_completed:
        # Extra check: if course requires final quiz, ensure it's passed
        if not course.requires_final_quiz or progress.final_quiz_passed:
            is_now_completed = True
            
    if is_now_completed:
        progress.is_completed = True
        progress.save()
        messages.success(request, f"Congratulations! You've completed the course: {course.title}")
        
    return render(request, 'lms/lesson_detail.html', {
        'lesson': lesson,
        'course': course
    })
