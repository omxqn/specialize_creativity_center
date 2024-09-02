from django.urls import path
from . import views


urlpatterns=[

path('', views.nurse_patient_prescription, name='nurse_patient_prescription'),
path('nurse_prescription_details/<int:id>', views.nurse_prescription_details, name='nurse_prescription_details'),

path('nurse_profile', views.nurse_profile, name='nurse_profile'),
















]