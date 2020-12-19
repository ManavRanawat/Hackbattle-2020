from django.db import models
from PIL import Image
from django.utils import timezone

from users.models import Profile
# Create your models here.
# from django.core.validators import RegexValidator
# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
# phone = forms.CharField(validators=[phone_regex], max_length=17)

class Hospital(models.Model):
    name=models.CharField(max_length=40)
    username=models.CharField(max_length=40)
    password=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    description=models.TextField(max_length=400,default="Welcome!")
    image=models.ImageField(upload_to='hospital_pics',default='default.jpg')
    phone_no=models.CharField(default=None,max_length=15)
    rating=models.IntegerField(default=3)

    def __str__(self):
        return self.username
'''
Pediatrician ->
 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid',

Cardiologist->
'Chronic cholestasis', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',  'Osteoarthristis', 'Arthritis',

Gynecologist->
'Cervical spondylosis','(vertigo) Paroymsal  Positional Vertigo', 'Urinary tract infection',

Internist->
Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Gastroenteritis', 'Paralysis (brain hemorrhage)'

Dermatologist->
'Acne', 'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae', 'AIDS'

Family Medicine->
'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
'''
class Speciality(models.Model):
    username=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    diff_spec=(
        ('1','Pediatrician'),
        ('2','Cardiologist'),
        ('3','Gynecologist'),
        ('4','Internist'),
        ('5','Dermatologist'),
        ('6','Family Medicine')
    )
    speciality=models.CharField(choices=diff_spec,max_length=100,default=6)

    def __str__(self):
        return self.username.name

class Appointment(models.Model):
    hname=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    accepted=models.BooleanField()
    date_of_appt=models.DateTimeField(default=None)

    def __str__(self):
        return self.hname.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
