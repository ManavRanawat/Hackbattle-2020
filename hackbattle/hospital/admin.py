from django.contrib import admin
from .models import Hospital,Post,Speciality,Appointment
# Register your models here.
admin.site.register(Hospital)
admin.site.register(Post)
admin.site.register(Speciality)
admin.site.register(Appointment)