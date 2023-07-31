# quiz/urls.py
from django.urls import path
from . import views

app_name = 'recommend'
urlpatterns = [
    path('', views.index, name='index'),
    path('loading/', views.loading, name='loading'),
    path('prog', views.prog, name='prog'),
    path('end', views.end, name='end'),
]