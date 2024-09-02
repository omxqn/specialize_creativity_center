from django.contrib import admin

from doctor.models import Appointment
from patient.models import Prescription
from .models import *

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Prescription)