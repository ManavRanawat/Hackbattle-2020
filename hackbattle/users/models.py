
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_hospital=models.BooleanField(default=False)
    # def __str__(self):
    #     return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)




class PatientRecord(models.Model):
    patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    symptom1=models.CharField(max_length=40,null=True)
    symptom2=models.CharField(max_length=40,null=True)
    symptom3=models.CharField(max_length=40,null=True)
    symptom4=models.CharField(max_length=40,null=True)
    disease_detected=models.CharField(max_length=40,null=True)
    date=models.DateTimeField(default=timezone.now)

class Hospital(models.Model):
    name=models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
    email=models.EmailField(max_length=100)
    description=models.TextField(max_length=400,default="Welcome!")
    # image=models.ImageField(upload_to='hospital_pics',default='default.jpg')
    phone_no=models.CharField(default=None,max_length=15,null=True)
    rating=models.IntegerField(default=3)

    # def __str__(self):
    #     return self.id
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
        ('Pediatrician','Pediatrician'),
        ('Cardiologist','Cardiologist'),
        ('Gynecologist','Gynecologist'),
        ('Internist','Internist'),
        ('Dermatologist','Dermatologist'),
        ('Family Medicine','Family Medicine')
    )
    speciality=models.CharField(choices=diff_spec,max_length=100,default=6)

    # def __str__(self):
    #     return self.username.name

class Appointment(models.Model):
    hname=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return self.hname.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title
    
class Chat(models.Model):
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    sender=models.CharField(max_length=15,default="Patient")
    message=models.CharField(max_length=300)
    date=models.DateTimeField(default=timezone.now)
    # def __str__(self):
    #     return self.message

class ScanCT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)
    ct_scan=models.ImageField(upload_to='report', blank= True,null=True)

    def get_absolute_url(self):
        return reverse('report-ct')

class ScanXRay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)
    xray=models.ImageField(upload_to='report', blank= True,null=True)

    def get_absolute_url(self):
        return reverse('report-xray')


