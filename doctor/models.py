from django.contrib.auth.models import User
from django.db import models

from patient.models import Patient


# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True)

    deposit_paid = models.CharField(max_length=2500,null=True,blank=True)
    fee_paid = models.CharField(max_length=2500,null=True,blank=True)
    remarks = models.CharField(max_length=2500,null=True,blank=True)
    created_by = models.CharField(max_length=2500,null=True,blank=True)
    appointment_at = models.DateTimeField(auto_now=True,editable=True)
    created_at = models.DateTimeField(auto_now=True,editable=True)

    doctor = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

