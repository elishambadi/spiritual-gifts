from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class SpiritualGift(models.Model):
    """Represents a spiritual gift category."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Question(models.Model):
    """Survey questions mapped to spiritual gifts."""
    number = models.IntegerField(unique=True)
    text = models.TextField()
    spiritual_gift = models.ForeignKey(
        SpiritualGift, 
        on_delete=models.CASCADE,
        related_name='questions'
    )
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return f"Q{self.number}: {self.text[:50]}..."


class SurveyResponse(models.Model):
    """Stores a complete survey submission."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Survey Response {self.id} - {self.created_at}"
    
    def calculate_results(self):
        """Calculate spiritual gift scores for this response."""
        gift_scores = {}
        
        for answer in self.answers.all():
            gift_name = answer.question.spiritual_gift.name
            if gift_name not in gift_scores:
                gift_scores[gift_name] = 0
            gift_scores[gift_name] += answer.rating
        
        return sorted(gift_scores.items(), key=lambda x: x[1], reverse=True)


class Answer(models.Model):
    """Individual answer for a question in a survey response."""
    survey_response = models.ForeignKey(
        SurveyResponse,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating: 5=Highly characteristic, 4=Most of the time, 3=Frequently, 2=Occasionally, 1=Not at all"
    )
    
    class Meta:
        unique_together = ['survey_response', 'question']
        ordering = ['question__number']
    
    def __str__(self):
        return f"Answer to Q{self.question.number} - Rating: {self.rating}"
