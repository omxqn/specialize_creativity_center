from django.urls import path
from . import views


urlpatterns=[
path('', views.doctor_dashboard, name='doctor_dashboard'),

path('doctor_patients', views.doctor_patients, name='doctor_patients'),

path('doctor_appointments', views.doctor_appointments, name='doctor_appointments'),
path('doctor_add_medicine', views.doctor_add_medicine, name='doctor_add_medicine'),
path('doctor_add_lab_test', views.doctor_add_lab_test, name='doctor_add_lab_test'),
path('doctor_add_prescription/<int:id>', views.doctor_add_prescription, name='doctor_add_prescription'),
path('doctor_delete_medicie/<int:medicine_id>/<int:appoint_id>', views.doctor_delete_medicie, name='doctor_delete_medicie'),
path('doctor_delete_test/<int:medicine_id>/<int:appoint_id>', views.doctor_delete_test, name='doctor_delete_test'),
path('doctor_profile', views.doctor_profile, name='doctor_profile'),














]