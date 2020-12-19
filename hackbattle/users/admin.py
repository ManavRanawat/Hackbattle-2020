  
from django.contrib import admin
from .models import (Profile,PatientRecord,Hospital,Post,Speciality,Chat,Appointment)

admin.site.register(Profile)
admin.site.register(PatientRecord)
admin.site.register(Hospital)
admin.site.register(Post)
admin.site.register(Speciality)
admin.site.register(Appointment)
admin.site.register(Chat)