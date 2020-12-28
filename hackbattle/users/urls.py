from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import users.views as views
from users.views import *


urlpatterns = [
    path('doctor/',views.register,name='ai-doctor'),
    # path('chat/<int:pk>/',views.,name='chat'),
    # path('<int:pk>/chathospital/',views.chatsection_hospital,name='chat_hospital'),
    path('chat/<int:pk>/<str:usrtype>',views.ChatSectionUserView.as_view(),name='chat'),
    path('patientschat/',views.patientslist,name='patients_chat'),
    # path('register-hospital/',views.register_hospital,name='register-hospital'),
    # path('',views.home,name="home"),
    path('hospitals/',views.dashboard,name="hospitals"),
    path('disease/',views.disease,name="disease"),
    path('suggested/<str:specialist>',views.suggestedspecialist,name='suggested-specialist'),
    path('ct_report/',views.report_ct,name='report-ct'),
    path('xray_report/',views.report_xray,name='report-xray'),
    path('scanct_form/', CTCreateView.as_view(), name='ct-create'),
    path('scanxray_form/', XrayCreateView.as_view(), name='xray-create'),
    path('addspeciality/',views.addspeciality,name='addspeciality'),
    path('hospital_recommend/',views.hospital_recommend,name='hospital-recommend'),

    path('records/',views.records,name='previous-records'),
]