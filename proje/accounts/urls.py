from django.urls import path

from . import views

urlpatterns = [
    path('login',views.login, name='login') ,
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('<int:class_id>',views.dashclass, name='dashclass'),
    path('createClass',views.createClass, name = 'createClass'),
    path('answerq',views.answerq, name = 'answerq'),
    path('setowner',views.setOwner, name='setowner'),
    path('numq',views.numq, name='numq'),
    path('crq',views.crq, name = 'crq'),
    path('convas',views.convas, name='convas'),
    path('taq/<int:class_id>',views.takeQ, name='takeQ'),
    path('seeq/<int:class_id>',views.seeQ, name='seeQ'),
    path('own/<int:class_id>',views.dashOwner, name='dashOwner'),
    path('seeEachQuiz',views.seeEachQuiz, name='seeEachQuiz'),
    path('seeEachQuizOwner',views.seeEachQuizOwner, name='seeEachQuizOwner'),
    path('delClass',views.delClass, name='delClass'),
    path('delStd',views.delStd, name='delStd'),
    path('seejQ',views.seejQ, name='seejQ'),
    path('delQ',views.delQ, name='delQ'),
    path('change',views.change, name='change'),
    path('activeQ',views.activeQ, name='activeQ'),
    path('changeProfile',views.changeProfile, name='changeProfile'),
]