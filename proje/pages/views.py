from django.shortcuts import render

from django.http import HttpResponse
from classes.models import Class

def index(request):
    classes = Class.objects.order_by('-classcreated_date')[:3]
    print(classes)
    creators = []
    classwithcreator = []
    for myclass in classes:
        print(myclass)
        if myclass.isPrivate:
            creator = myclass.userclassrelation_set.filter(isCreator=True)[0].user.first_name
            classwithcreator.append(tuple((myclass,creator,"1")))
        else:
            creator = myclass.userclassrelation_set.filter(isCreator=True)[0].user.first_name
            classwithcreator.append(tuple((myclass,creator,"0")))
    
    context = {
        'classwithcreator' : classwithcreator,
    }
    return render(request,'pages/index.html',context)

    
def about(request):
    return render(request,'pages/about.html')
