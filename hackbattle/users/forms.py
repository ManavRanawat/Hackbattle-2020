from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Hospital,Speciality,Post,Appointment
from django import forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_hospital=forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'is_hospital', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class HospitalUpdateForm(forms.ModelForm):
	# description=forms.CharField(max_length=400)
	class Meta:
		model = Hospital
		fields = ['name','email','description','phone_no']

class SpecialityUpdateForm(forms.ModelForm):

    class Meta:
        model = Speciality
        fields = ['speciality']