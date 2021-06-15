from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth.models import User ,auth
from classes.models import Class
from userclassrelations.models import Userclassrelation 
from quizes.models import Quiz
from . import views
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from singlequestions.models import Singlequestion


def register(request):
    if(request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']   
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is Taken')
                return redirect('register')
            else: 
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password,
                    email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request,'You are now registered and can log in')
                    return redirect('login')

                    return
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')
    
def login(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')
    
def logout(request):
    if(request.method == 'POST'):
        auth.logout(request)
        messages.success(request,'You are logged out')
        return redirect('index')

def createClass(request):
    if request.method == 'POST':
        title = request.POST['title']        
        description = request.POST['discription']
        class_day = request.POST['class_day']
        class_time = request.POST['class_time']
        moreabout = request.POST['moreabout']
        password = request.POST['password']

        user = request.user
        if password:
            oneclass = Class(title = title, description = description, class_time = class_time, class_day = class_day,isPrivate=True,Password=password)
        else:
            oneclass = Class(title = title, description = description, class_time = class_time, class_day = class_day)
            
        oneclass.save()

        userclassrelation = Userclassrelation(user=user, myclass=oneclass, isCreator=True, description=moreabout)
        userclassrelation.save()
        messages.success(request,"new class is created")
        return redirect('dashboard')


def dashboard(request):
    myuser = request.user
    userclassrelations = Userclassrelation.objects.filter(user = myuser)
    students = []
    creators = []
    owners = []
    numofquizes = 0
    numberofstudents = 0
    classwithcreator=[]
    classwithstunumandquiz = [] #class + tedad student + tedad quiz
    classwithstunumandowner = []
    classwithquiznum = [] #gharare moshakhaskone taken hast ya na
    quiznums = []
    # creatorquizes = []
    # ownerquizes = []
    # studentquizes = []
    for userclassrelation in userclassrelations:
        if userclassrelation.isCreator:
            creators.append(userclassrelation.myclass)
        elif userclassrelation.isStudent:
            students.append(userclassrelation.myclass)
        elif userclassrelation.isOwner:
            owners.append(userclassrelation.myclass)

    for myclass in creators:
        numberofstudents=0
        numofquizes=0
        for quiz in myclass.quiz_set.all():
            numofquizes+=1
        for singleuserclassrelation in myclass.userclassrelation_set.all():
            if singleuserclassrelation.isStudent:
                numberofstudents+=1
        classwithstunumandquiz.append(tuple((myclass,numberofstudents,numofquizes)))

    for myclass in owners:
        numberofstudents=0
        numofquizes=0
        for quiz in myclass.quiz_set.all():
            numofquizes+=1
        for singleuserclassrelation in myclass.userclassrelation_set.all():
            if singleuserclassrelation.isStudent:
                numberofstudents+=1
        classwithstunumandowner.append(tuple((myclass,numberofstudents,numofquizes)))
    
    numoftakenquizes=0
    numofquizes=0
    studentindex=0
    quizindex=0


    for myclass in students:
        studentindex = 0
        numoftakenquizes=0
        numofquizes=0
        for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
            if singleuserclassrelation.user == request.user:
                break
            else:
                studentindex = studentindex + 1

        for quiz in myclass.quiz_set.all():
            if quiz.taken[studentindex]:
                numoftakenquizes+=1
            elif quiz.isActive:
                numofquizes+=1

        classwithquiznum.append(tuple((myclass,numofquizes,numoftakenquizes,myclass.userclassrelation_set.filter(isCreator=True)[0].user.username)))


    context = {
        'classwithquiznum' : classwithquiznum,
        'classwithstunumandowner' : classwithstunumandowner,
        'classwithstunumandquiz' : classwithstunumandquiz,
    }
    
    return render(request,'accounts/dashboard.html',context)


def dashclass(request,class_id):
    myclass = Class.objects.filter(id=class_id)[0]
    students = []
    owneruser = []
    classids = []
    quizwithstat = []
    for userclassrelation in myclass.userclassrelation_set.all():
        if userclassrelation.isStudent:
            students.append(userclassrelation.user)



    owners = myclass.userclassrelation_set.filter(isOwner=True)
    for owner in owners:
        owneruser.append(owner.user)    
    classids.append(class_id)
    quizs = myclass.quiz_set.all().order_by('quizcreated_date')
    for quiz in quizs:
        if quiz.isActive:
            quizwithstat.append(tuple((quiz,"1")))
        else:
            quizwithstat.append(tuple((quiz,"0")))

    context = {
        'owneruser' : owneruser,
        'class_id' : classids,
        'students' : students,
        'quizes' : quizwithstat,
        }

    return render(request,'accounts/dashclass.html',context)
    
def setOwner(request):
    if(request.method == 'GET'):
        classid = request.GET['classid']
        owner = request.GET['owner']
        oneclass = Class.objects.filter(id=classid)[0]
        owneruser = User.objects.filter(username=owner)[0]
        userclassrelation = Userclassrelation(user=owneruser, myclass=oneclass, isOwner=True)
        userclassrelation.save()
        messages.success(request,'owner set successfully')
        return HttpResponseRedirect(reverse('dashclass',args=[classid]))


def numq(request):
    if(request.method == 'GET'):
        classid = request.GET['classid']
        numq = request.GET['numq']
        oneclass = Class.objects.filter(id=classid)[0]
        indexes = []
        classes = []
        if int(numq) >= 1:
            for i in range(1,int(numq)+1):
                indexes.append(i)
        

        classes.append(int(classid))
        quizes = oneclass.quiz_set.all()
        context= {
            'quizes': quizes,
            'indexes' : indexes,
            'classes' : int(classid),
        }
        return render(request,'accounts/createquiz.html',context)

def crq(request):
    if(request.method == "POST"):
        number = request.POST["num"]
        title = request.POST["title"]
        classid = request.POST["classid"]
        answers=[]
        questions = []
        for i in range(1,int(number)+1):
            questions.append(request.POST['Q'+str(i)])


        myquiz = Quiz(title = title,number=int(number), myclass = Class.objects.filter(id=classid)[0])
        myquiz.taken=[]
    
        for student in Class.objects.filter(id=classid)[0].userclassrelation_set.filter(isStudent=True):
            myquiz.taken.append(False)
            answers.append('')
            

        myquiz.save()

        for question in questions:
            singlequestions = Singlequestion(quiz=myquiz,question=question,answers=answers)
            singlequestions.save()
    messages.success(request,'Quiz created successfully')

    return HttpResponseRedirect(reverse('dashclass',args=[classid]))

def takeQ(request,class_id):
    myclass = Class.objects.filter(id=class_id)[0]
    quizes = Quiz.objects.filter(myclass=myclass).order_by('quizcreated_date')
    untakenquizes=[]
    questions=[]

    studentindex = 0

    for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
        if singleuserclassrelation.user == request.user:
            break
        else:
            studentindex = studentindex + 1

    index = 1
    for quiz in quizes:
        if quiz.isActive:
            print(quiz.taken[studentindex])
            if not quiz.taken[studentindex]:
                print(quiz.isActive)
                untakenquizes.append(quiz)
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    print(untakenquizes)
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIII")
    if untakenquizes:
        for question in untakenquizes[0].singlequestion_set.all():
            questions.append(tuple((question,index)))
            index += 1
    
    if untakenquizes:
        untake = untakenquizes[0]
    else:
        untake=[]

    if not len(questions):
        messages.error(request,'No Active Untaken Quizes Yet')
        return redirect('dashboard')

    context = {
        'classid' :class_id,
        'untakenquizes': untake,
        'questions' : questions
    }

    return render(request,'accounts/takequiz.html',context)


def answerq(request):
    if(request.method == "POST"):
        quizid = request.POST['quizid']
        classid = request.POST['classid']
        myclass = Class.objects.filter(id=classid)[0]
        numberofquesions = Quiz.objects.filter(id=quizid)[0].number
        myquiz = Quiz.objects.filter(id=quizid)[0]

        studentindex=0

        for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
            if singleuserclassrelation.user == request.user:
                break
            else:
                studentindex = studentindex + 1

        index = 1
        for singlequestion in myquiz.singlequestion_set.all():
            singlequestion.answers[studentindex] = request.POST["Q"+str(index)]
            index+=1
            singlequestion.save()
        
        myquiz.taken[studentindex] = True
        myquiz.save()

        messages.success(request,"Answers Successfully Submited")
    
        return redirect('dashboard')

def seeQ(request,class_id):
    myclass = Class.objects.filter(id=class_id)[0]
    questions = []
    takenquizes=[]
    quiznumbers=[]
    numbers = []
    newlist=[]
    titles = []
    integers=[]

    studentindex = 0
    for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
        if singleuserclassrelation.user == request.user:
            break
        else:
            studentindex = studentindex + 1

    for onequiz in Quiz.objects.filter(myclass=myclass).order_by('-quizcreated_date'):
        if onequiz.taken[studentindex]:
            takenquizes.append(onequiz)
            quiznumbers.append(onequiz.number)
            titles.append(onequiz.title)
    for num in quiznumbers:
        for i in range(1,num+1):
            numbers.append(str(i))
        

    index = 0
    for num,title in zip(quiznumbers,titles):
        for i in range(index,int(num)- 1):
            titles.insert(i,title)
        index = index + int(num) - 1


    print(takenquizes)
    for quiz in takenquizes:
        for singlequestion,number,title in zip(quiz.singlequestion_set.all(),numbers,titles):
            questions.append(tuple((singlequestion.question,singlequestion.answers[studentindex],number,title)))


    if not len(takenquizes):
        messages.error(request,'No Taken Quizes Yet')
        return redirect('dashboard')
    

    context={
        'questions' : questions,
    }

    return render(request,'accounts/seequiz.html',context)


def seeEachQuiz(request):
    class_id = request.GET['classid']
    myclass = Class.objects.filter(id=request.GET['classid'])[0]
    user = User.objects.filter(id=request.GET['studentid'])[0]
    questions = []
    takenquizes=[]
    quiznumbers=[]
    numbers = []
    newlist=[]
    titles = []
    integers=[]

    studentindex = 0
    for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
        if singleuserclassrelation.user == user:
            break
        else:
            studentindex = studentindex + 1

    for onequiz in Quiz.objects.filter(myclass=myclass).order_by('-quizcreated_date'):
        if onequiz.taken[studentindex]:
            takenquizes.append(onequiz)
            quiznumbers.append(onequiz.number)
            titles.append(onequiz.title)

    for num in quiznumbers:
        for i in range(1,num+1):
            numbers.append(str(i))
        

    index = 0
    for num,title in zip(quiznumbers,titles):
        for i in range(index,int(num)- 1):
            titles.insert(i,title)
        index = index + int(num) - 1

    for quiz in takenquizes:
        for singlequestion,number,title in zip(quiz.singlequestion_set.all(),numbers,titles):
            questions.append(tuple((singlequestion.question,singlequestion.answers[studentindex],number,title)))

    if not len(takenquizes):
        messages.error(request,'No Taken Quizes Yet')
        return HttpResponseRedirect(reverse('dashclass',args=[class_id]))

    context={
        'questions' : questions,
    }
    print(questions)

    return render(request,'accounts/seequiz.html',context)

def seejQ(request):
    quiz_id = request.GET['quizid']
    myquiz = Quiz.objects.filter(id=request.GET['quizid'])[0]
    questions=[]
    index=1

    for question in myquiz.singlequestion_set.all():
        questions.append(tuple((question,index)))
        index+=1
    
    context={
        'title' : myquiz.title,
        'questions' : questions,
    }
    print('hi')
    return render(request,'accounts/seejQ.html',context)

def delQ(request):
    myquiz = Quiz.objects.filter(id=request.GET['quizid'])[0]
    classid = request.GET['classid']
    myquiz.delete()
    messages.success(request,myquiz.title + " quiz successfully deleted")
    return HttpResponseRedirect(reverse('dashclass',args=[classid]))


def delClass(request):
    class_id = request.GET['classid']
    myclass = Class.objects.filter(id=request.GET['classid'])[0]
    myclass.delete()
    messages.success(request,myclass.title + " class successfully deleted")
    return redirect('dashboard')

def dashOwner(request,class_id):
    myclass = Class.objects.filter(id=class_id)[0]
    students = []
    owneruser = []
    classids = []
    for userclassrelation in myclass.userclassrelation_set.all():
        if userclassrelation.isStudent:
            students.append(userclassrelation.user)



    owners = myclass.userclassrelation_set.filter(isOwner=True)
    for owner in owners:
        owneruser.append(owner.user)    
    classids.append(class_id)
    quizs = myclass.quiz_set.all() 
    print(owneruser)
    print("hi")
    context = {
        'owneruser' : owneruser,
        'class_id' : classids,
        'students' : students,
        'quizes' : quizs,
        }

    return render(request,'accounts/dashowner.html',context)


def seeEachQuizOwner(request):
    class_id = request.GET['classid']
    myclass = Class.objects.filter(id=request.GET['classid'])[0]
    user = User.objects.filter(id=request.GET['studentid'])[0]
    questions = []
    takenquizes=[]
    quiznumbers=[]
    numbers = []
    newlist=[]
    titles = []
    integers=[]

    studentindex = 0
    for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
        if singleuserclassrelation.user == user:
            break
        else:
            studentindex = studentindex + 1

    for onequiz in Quiz.objects.filter(myclass=myclass).order_by('-quizcreated_date'):
        if onequiz.taken[studentindex]:
            takenquizes.append(onequiz)
            quiznumbers.append(onequiz.number)
            titles.append(onequiz.title)
    print(takenquizes)
    print(quiznumbers)
    for num in quiznumbers:
        for i in range(1,num+1):
            numbers.append(str(i))
        

    index = 0
    for num,title in zip(quiznumbers,titles):
        for i in range(index,int(num)- 1):
            titles.insert(i,title)
        index = index + int(num) - 1

    for quiz in takenquizes:
        for singlequestion,number,title in zip(quiz.singlequestion_set.all(),numbers,titles):
            questions.append(tuple((singlequestion.question,singlequestion.answers[studentindex],number,title)))

    if not len(takenquizes):
        messages.error(request,'No Taken Quizes Yet')
        return HttpResponseRedirect(reverse('dashOwner',args=[class_id]))

    context={
        'questions' : questions,
    }

    return render(request,'accounts/seequiz.html',context)

def change(request):

    return render(request,'accounts/changeProfile.html')

def changeProfile(request):
    if(request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']   
        user = request.user
        if password == password2:
            if User.objects.filter(username=username).exists():
                if not request.user.username == username:
                    messages.error(request, 'That username is Taken')
                    return redirect('change')
                else:
                    user.username = username
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.set_password(password)
                    user.save()
                    if user is not None:
                        auth.login(request,user)
                    messages.success(request,'Your information has changed successfully')
                    return redirect('change')
            else: 
                if User.objects.filter(email=email).exists():
                    if not request.user.email == email:
                        messages.error(request, 'That email is used')
                        return redirect('change')
                    else:
                        user.username = username
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email
                        user.set_password(password)
                        user.save()
                        if user is not None:
                            auth.login(request,user)
                        messages.success(request,'Your information has changed successfully')
                        return redirect('change')
                else:
                    user.username = username
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.set_password(password)
                    user.save()
                    if user is not None:
                        auth.login(request,user)
                    messages.success(request,'Your information has changed successfully')
                    return redirect('change')

                    return
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('change')
    else:
        return render(request,'accounts/changeProfile.html')

def delStd(request):
    class_id = request.GET['class_id2']
    studentid = request.GET['studentid2']
    std = User.objects.filter(id = studentid)[0]
    myclass = Class.objects.filter(id = class_id)[0]

    studentindex = 0
    for singleuserclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
        if singleuserclassrelation.user == std:
            break
        else:
            studentindex = studentindex + 1
    for userclassrelation in myclass.userclassrelation_set.filter(isStudent=True):
        if(userclassrelation.user == std):
            userclassrelation.delete()
            messages.success(request,userclassrelation.user.username + " user successfully deleted")

    
    for quiz in myclass.quiz_set.all():
        print("HIIIIIIIIIIIIIIIIIIIIIIIII")
        print(quiz.taken[studentindex])
        print("HIIIIIIIIIIIIIIIIIIIIIIII")
        for singlequestion in quiz.singlequestion_set.all():
            del singlequestion.answers[studentindex]
            singlequestion.save()
        del quiz.taken[studentindex]
        quiz.save()


    return HttpResponseRedirect(reverse('dashclass',args=[class_id]))

def activeQ(request):
    quiz_id = request.GET['quizid3']
    class_id = request.GET['class_id3']
    quiz = Quiz.objects.filter(id = quiz_id)[0]    
    myclass = Class.objects.filter(id = class_id)[0]
    if quiz.isActive:
        quiz.isActive=False
    else:
        quiz.isActive=True
    quiz.save()
    return HttpResponseRedirect(reverse('dashclass',args=[class_id]))

def convas(request):
    return render(request,'accounts/canvas.html')
    