from django.db import models
from datetime import datetime
from quizes.models import Quiz
from django.contrib.postgres.fields import ArrayField
class Singlequestion(models.Model):
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    answers =  ArrayField(
            models.CharField(max_length=300, blank=True),default=[]
    )
    def __str__(self):
        return self.question