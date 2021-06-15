from django.db import models
from classes.models import Class
from datetime import datetime
from django.contrib.postgres.fields import ArrayField


class Quiz(models.Model):
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    descriprion = models.TextField(blank=True)
    number = models.IntegerField()
    quizcreated_date = models.DateTimeField(default=datetime.now)
    quizduration = models.IntegerField(default=2)
    isActive = models.BooleanField(default=False)
    grades =  ArrayField(
        models.DecimalField(max_digits=4, decimal_places=1),default=[]
    )
    taken =  ArrayField(
        models.BooleanField(default=False),default=[]
    )


    def __str__(self):
        return self.title

