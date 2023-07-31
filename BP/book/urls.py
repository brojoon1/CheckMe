# book/urls.py
from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.list, name='list'),
    path('detail', views.detail, name='detail'),
    path('detail/<isbn>', views.detail, name='detail'),
    path('child', views.list_child, name='list_child'),
]