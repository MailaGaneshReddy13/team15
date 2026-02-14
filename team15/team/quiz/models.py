from django.db import models
from django.conf import settings

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    topic = models.CharField(max_length=255)
    score = models.IntegerField()
    total_questions = models.IntegerField(default=30)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic} - {self.score}/{self.total_questions}"
