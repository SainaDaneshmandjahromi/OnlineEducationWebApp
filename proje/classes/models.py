from django.db import models
from datetime import datetime

class Class(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    classcreated_date = models.DateTimeField(default=datetime.now)
    class_day = models.CharField(max_length=200)
    class_time = models.CharField(max_length=200)
    isPrivate = models.BooleanField(default=False)
    Password = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.title