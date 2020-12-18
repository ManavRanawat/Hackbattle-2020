from django.db import models
from PIL import Image
from django.utils import timezone
# Create your models here.
# from django.core.validators import RegexValidator
class Hospital(models.Model):
    name=models.CharField(max_length=40)
    username=models.CharField(max_length=40)
    # address=None
    password=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone = forms.CharField(validators=[phone_regex], max_length=17)
    phone_no=models.CharField(default=None,max_length=15)
    rating=models.IntegerField(default=3)

    def __str__(self):
        return self.username

# class Speciality(models.Model):
#     username=models.ForeignKey(Hospital)
#     choices=(
#         ('1','General'),
#         ('2','Eye Specialist'),
#         ('3','')
#     )
#     speciality=models.choiceField(choices)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
