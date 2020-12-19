from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import users.views as views
urlpatterns = [
    path('doctor/',views.register,name='ai-doctor'),
    path('<int:pk>/chat/',views.chatsection,name='chat'),
    path('register-hospital/',views.register_hospital,name='register-hospital'),
    path('',views.home,name="home"),
    path('hospitals/',views.hospitals,name="hospitals")
]