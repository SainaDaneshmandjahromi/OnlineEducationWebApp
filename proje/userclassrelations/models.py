from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from classes.models import Class

class Userclassrelation(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    isCreator = models.BooleanField(default=False)
    isOwner = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    beingrelated =  models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username
