from django.contrib import admin

from patient.models import Prescription, Medicines
from pharamacy.models import Main_category

# Register your models here.


admin.site.register(Main_category)
admin.site.register(Medicines)