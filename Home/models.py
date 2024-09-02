from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, blank=True, unique=True, null=True)

    picture = models.ImageField(upload_to='ProfilImages', blank=True)



    gender = models.CharField(max_length=25, blank=True, null=True)

    role = models.CharField(max_length=2500, blank=True, null=True)
    specialization = models.CharField(max_length=2500, blank=True, null=True)
    availablity_from = models.DateTimeField( blank=True, null=True)
    availablity_to = models.DateTimeField( blank=True, null=True)



    otp = models.CharField(max_length=25, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')