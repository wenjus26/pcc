import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.citizens.models import CitizenProfile, Skill

class Badge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fas fa-award')
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Evaluation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='evaluations')
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=15)
    passing_score = models.PositiveIntegerField(default=70) # Percentage
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.skill.name})"

class Question(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text[:50]

class UserResult(models.Model):
    profile = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='evaluation_results')
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    score = models.FloatField() # Percentage
    completed_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.evaluation.title} ({self.score}%)"
