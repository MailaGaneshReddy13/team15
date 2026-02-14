from django.db import models
from django.conf import settings

class Job(models.Model):
    hr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField(help_text="Comma separated skills")
    experience_required = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resume(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    parsed_data = models.JSONField(null=True, blank=True)
    match_score = models.FloatField(default=0.0)
    ai_feedback = models.TextField(blank=True, null=True)
    skills_matched = models.TextField(blank=True, null=True)
    missing_skills = models.TextField(blank=True, null=True)
    improvement_suggestions = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume of {self.candidate.username}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True)
    match_score = models.FloatField(default=0.0)
    ai_feedback = models.TextField(blank=True, null=True)
    skills_matched = models.TextField(blank=True, null=True)
    missing_skills = models.TextField(blank=True, null=True)
    improvement_suggestions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"

    @property
    def upcoming_live_interview(self):
        return self.live_interviews.filter(status='scheduled').first()
