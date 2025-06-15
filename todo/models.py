from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone

class Task(models.Model):
    task = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1, "Task cannot be empty"),
            MaxLengthValidator(200, "Task cannot exceed 200 characters")
        ],
        help_text="Enter your task (max 200 characters)"
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.task}"
    
    def save(self, *args, **kwargs):
        # Clean the task text
        self.task = self.task.strip()
        super().save(*args, **kwargs)