from django.urls import path

from . import views

urlpatterns = [
    path('<int:class_id>',views.moreInfo, name='class'),
    path('search',views.search, name='search'),
    path('enrol',views.enrol, name='enrol'),
    path('notenrol',views.notenrol, name='notenrol'),
]