from django.db import models
from django.conf import settings

class Course(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical Skills'),
        ('soft_skills', 'Soft Skills'),
        ('career_prep', 'Career Preparation'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='technical')
    requires_final_quiz = models.BooleanField(default=True)
    final_quiz_topic = models.CharField(max_length=255, blank=True, null=True, help_text="The topic string to use for the AI quiz generation for this course.")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.final_quiz_topic:
            self.final_quiz_topic = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def total_modules(self):
        return self.modules.count()

    @property
    def total_lessons(self):
        return Lesson.objects.filter(module__course=self).count()

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Lesson content (HTML/Text)")
    duration_minutes = models.IntegerField(default=10, help_text="Estimated reading time")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class UserCourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    final_quiz_passed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    @property
    def progress_percent(self):
        total_lessons = self.course.total_lessons
        if total_lessons == 0:
            return 100 if (not self.course.requires_final_quiz or self.final_quiz_passed) else 0
            
        completed_lessons_count = self.completed_lessons.count()
        
        if self.course.requires_final_quiz:
            # 90% from lessons, 10% from quiz
            lessons_progress = (completed_lessons_count / total_lessons) * 90
            quiz_progress = 10 if self.final_quiz_passed else 0
            return int(lessons_progress + quiz_progress)
        else:
            return int((completed_lessons_count / total_lessons) * 100)
