from django.db import models

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    ]


    user_email = models.EmailField()
    task = models.CharField(max_length=255) # can be textfield for large amt of text
    due_by = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.task