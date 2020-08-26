from django.urls import path, include
from django.contrib.auth import views
# from django.contrib.auth.views import login, logout
from .views import *


urlpatterns = [
    path('options/'              , OptionsCreate.as_view(), name = "options_create_url"),
    path('home/'                 , HomeView.as_view()),
    path(r'check_record/<int:id>', Check_record.as_view(), name = "check_record"),
    path(r'seach/'               , Filter.as_view(), name = "find"),
    path(r'del/'                 , Delete_humans.as_view(), name = "del_hum"),
    path(r'info/'                 , Info.as_view(), name = "info"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
