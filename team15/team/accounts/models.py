from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('hr', 'HR (Recruiter)'),
        ('candidate', 'Candidate (Student/Job Seeker)'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    phone = models.CharField(max_length=15, blank=True, null=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True, help_text="Required for HR role")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def total_applicants(self):
        from jobs.models import Application
        return Application.objects.filter(job__hr=self).count()

    @property
    def interviews_scheduled_count(self):
        return self.job_applications.filter(status='interview').count()
