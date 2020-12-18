
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



class PatientRecord(models.Model):
    patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    symptom1=models.CharField(max_length=40)
    symptom2=models.CharField(max_length=40)
    symptom3=models.CharField(max_length=40)
    symptom4=models.CharField(max_length=40)
    ct_scan=models.ImageField(upload_to='report_pics')
    ct_scan=models.ImageField(upload_to='report_pics')
    disease_detected=models.CharField(max_length=40)
    date=models.DateTimeField(default=timezone.now)
