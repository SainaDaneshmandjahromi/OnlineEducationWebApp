from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Class
from django.contrib import messages
from userclassrelations.models import Userclassrelation
from django.contrib.auth.models import User ,auth
from quizes.models import Quiz
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

def moreInfo(request,class_id):
    myclass = get_object_or_404(Class, pk = class_id)
    creator = myclass.userclassrelation_set.filter(isCreator=True)[0]
    myuser = creator.user
    pv = []
    if myclass.isPrivate:
        pv.append(True)
    context = {
        'pv' : pv,
        'myclass' : myclass,
        'creator' : creator,
        'myuser' : myuser,
    }

    return render(request,'classes/moreInfo.html',context)


def search(request):
    if request.method == 'GET':
        

        classes = Class.objects.order_by('-classcreated_date')
        creators = Userclassrelation.objects.filter(isCreator=True)
        classwithcreator = []

        usercreators = []
        for creator in creators:
            usercreators.append(creator.user)

        for myclass in classes:
            creatornames = myclass.userclassrelation_set.filter(isCreator=True)[0].user.username
            classwithcreator.append(tuple((myclass,creatornames)))

        newusers = usercreators

        if 'keywords' in request.GET:
            keywords = request.GET['keywords']
            if keywords: 
                classwithcreator = []
                classes = classes.filter(description__icontains=keywords)
                creators = creators.filter(description__icontains=keywords)
                usercreators = []
                newusers = []
                for creator in creators:
                    usercreators.append(creator.user)
                    newusers.append(creator.user)
                for myclass in classes:
                    creatoruser = myclass.userclassrelation_set.filter(isCreator=True)[0].user
                    if creatoruser in usercreators:
                        usercreators.remove(creatoruser)
                        newusers.remove(creatoruser)
                    classwithcreator.append(tuple((myclass,creatoruser.username)))
                for creatoruser in usercreators:
                    classwithcreator.append(tuple((creatoruser.userclassrelation_set.filter(description__icontains=keywords)[0].myclass,creatoruser.username)))
                for myclass in classes:
                    usercreators.append(myclass.userclassrelation_set.filter(isCreator=True)[0].user)
                    newusers.append(myclass.userclassrelation_set.filter(isCreator=True)[0].user)


        if 'creator' in request.GET:
            creator = request.GET['creator']
            if creator:
                classwithcreator = []
                newusers = []
                for usercreator in usercreators:
                    if usercreator.username == creator:
                        newusers.append(usercreator)
                for newuser in newusers:
                    userclassrelations = newuser.userclassrelation_set.filter(isCreator=True)
                    if keywords:
                        userclassrelations = userclassrelations.filter(description__icontains=keywords)
                for oneuserclassrelation in userclassrelations:
                    classwithcreator.append(tuple((oneuserclassrelation.myclass,oneuserclassrelation.user.username)))
 
        if 'title' in request.GET:
            title = request.GET['title']
            if title:
                classes = []
                newclasses = []
                classwithcreator = []
                userclassrelationss = []
                newusers = list(dict.fromkeys(newusers))
                for newuser in newusers:
                    userclassrelationss.append(newuser.userclassrelation_set.filter(isCreator=True))
                for userclassrelations in userclassrelationss:
                    if keywords:
                        userclassrelations = userclassrelations.filter(description__icontains=keywords)
                    for userclassrelation in userclassrelations:
                        classes.append(userclassrelation.myclass)
                for singleclass in classes:
                    if singleclass.title == title:
                        newclasses.append(singleclass)
                for myclass in newclasses:
                    creatoruser = myclass.userclassrelation_set.filter(isCreator=True)[0].user.username
                    classwithcreator.append(tuple((myclass,creatoruser)))


                

        context = {
            'classwithcreator' : classwithcreator,
            'values' :request.GET
        }
        return render(request,'classes/search.html',context)


def notenrol(request):
    messages.error(request,'You have to login to enrol in classes')
    return redirect('register')


def enrol(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        class_id = request.POST['class_id']        
        email = request.POST['email']

        oneclass = Class.objects.filter(id = class_id)[0]
        user = User.objects.filter(id = user_id)[0]
        if oneclass.userclassrelation_set.filter(user_id = user_id).exists():
            messages.error(request,'You have been added to this class')
            return HttpResponseRedirect(reverse('class',args=[class_id]))
        else:            
            if oneclass.isPrivate:
                password = request.POST['password']
                if oneclass.Password != password:
                    messages.error(request,'Wrong Password')
                    return HttpResponseRedirect(reverse('class',args=[class_id]))
                else:
                    userclassrelation = Userclassrelation(user=user, myclass=oneclass, isStudent=True)
                    userclassrelation.save()
                    # send_mail(
                    #     'Enrolling in Class',
                    #     'You successfully enrolled in ' + oneclass.title + ' Sign in to see more Information',
                    #     'daneshmand.saina@gmail.com',
                    #     [user.email,'daneshmand.saina@gmail.com'],
                    #     fail_silently=False
                    # )
            
                    for quiz in Class.objects.filter(id=class_id)[0].quiz_set.all():
                        quiz.taken.append(False)
                        quiz.save()
                        for singlequestion in quiz.singlequestion_set.all():
                            singlequestion.answers.append('')
                            singlequestion.save()

                    messages.success(request,'Now You are a student of '+oneclass.title +' class')
                    return HttpResponseRedirect(reverse('class',args=[class_id]))
 

            else:
                userclassrelation = Userclassrelation(user=user, myclass=oneclass, isStudent=True)
                userclassrelation.save()
                # send_mail(
                #     'Enrolling in Class',
                #     'You successfully enrolled in ' + oneclass.title + ' Sign in to see more Information',
                #     'daneshmand.saina@gmail.com',
                #     [user.email,'daneshmand.saina@gmail.com'],
                #     fail_silently=False
                # )
                for quiz in Class.objects.filter(id=class_id)[0].quiz_set.all():
                    quiz.taken.append(False)
                    quiz.save()
                    for singlequestion in quiz.singlequestion_set.all():
                        singlequestion.answers.append('')
                        singlequestion.save()
            
                messages.success(request,'You are a student of '+oneclass.title +' class')
                return HttpResponseRedirect(reverse('class',args=[class_id]))
 