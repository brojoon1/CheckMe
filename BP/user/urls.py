# user_app/urls.py
from django.urls import path
from user import views
from django.contrib.auth import views as auth_views

app_name = 'user'
urlpatterns = [
    path('register/', views.user_form_view, name='register'),
    path('register/check-username/', views.check_username, name='check_username'),
    path('select/', views.select, name='select'),
    path('login/', views.login_view, name='login'),
    path('forgot_id/', views.forgot_id, name='forgot_id'),
    path('forgot_pw/', views.forgot_pw, name='forgot_pw'),
    path('forgot_pw/<str:uid>/<str:token>/', views.forgot_pw, name='forgot_pw'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('mypage/', views.mypage, name='mypage'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete_check, name='delete_check'),
    path('delete_/', views.delete_real, name='delete_real'),
]
