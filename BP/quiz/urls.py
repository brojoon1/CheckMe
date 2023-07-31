# quiz/urls.py
from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('prog', views.prog, name='prog'),
    path('end', views.end, name='end'),
]