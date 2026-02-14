from django.db import models
from django.conf import settings
from jobs.models import Job, Application

class InterviewSession(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    overall_score = models.FloatField(default=0.0)
    overall_feedback = models.TextField(blank=True, null=True)
    strengths = models.TextField(blank=True, null=True)
    improvements = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview of {self.candidate.username} for {self.job.title}"

class InterviewQuestion(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}..."

class InterviewAnswer(models.Model):
    question = models.OneToOneField(InterviewQuestion, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    score = models.FloatField(default=0.0)
    feedback = models.TextField(blank=True, null=True)
    strengths = models.TextField(blank=True, null=True)
    improvements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer to {self.question}"

class LiveInterview(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='live_interviews')
    interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conducted_interviews')
    scheduled_at = models.DateTimeField()
    meeting_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    duration_minutes = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Live Interview: {self.application.candidate.username} - {self.application.job.title}"

class AIInterviewSession(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_interviews')
    role = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=100)
    interview_type = models.CharField(max_length=100) # Technical, HR, etc.
    tech_stack = models.TextField()
    num_questions = models.IntegerField(default=5)
    
    vapi_call_id = models.CharField(max_length=255, blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    
    # Feedback Scores (0-100)
    communication_score = models.FloatField(default=0.0)
    technical_score = models.FloatField(default=0.0)
    problem_solving_score = models.FloatField(default=0.0)
    cultural_fit_score = models.FloatField(default=0.0)
    confidence_score = models.FloatField(default=0.0)
    clarity_score = models.FloatField(default=0.0)
    
    overall_score = models.FloatField(default=0.0)
    feedback_summary = models.TextField(blank=True, null=True)
    detailed_feedback = models.JSONField(blank=True, null=True)
    
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Interview: {self.candidate.username} - {self.role}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_cancelled', 'Interview Cancelled'),
        ('general', 'General'),
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='general')
    related_interview = models.ForeignKey(LiveInterview, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
