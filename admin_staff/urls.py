from django.urls import path
from . import views


urlpatterns=[
path('', views.admin_dashboard, name='admin_dashboard'),
path('create_account/', views.create_account, name='Sign_up'),
path('Settings', views.Setting, name='Settings'),
path('admin_patient_list_view', views.admin_patient_list_view, name='admin_patient_list_view'),
path('admin_doctor_list_view', views.admin_doctor_list_view, name='admin_doctor_list_view'),
path('admin_appointment_list_view', views.admin_appointment_list_view, name='admin_appointment_list_view'),
path('admin_add_appointment', views.admin_add_appointment, name='admin_add_appointment'),
path('admin_edit_appointment/<int:id>', views.admin_edit_appointment, name='admin_edit_appointment'),

path('admin_doctor_detail_view/<int:id>', views.admin_doctor_detail_view, name='admin_doctor_detail_view'),
#path('admin_doctor_edit_view/<int:id>', views.admin_doctor_edit_view, name='admin_doctor_edit_view'),
path('admin_add_patient', views.admin_add_patient, name='admin_add_patient'),
path('admin_patient_detail/<int:id>', views.admin_patient_detail, name='admin_patient_detail'),
path('admin_edit_patient/<int:id>', views.admin_edit_patient, name='admin_edit_patient'),
path('admin_appointment_detail/<int:id>', views.admin_appointment_detail, name='admin_appointment_detail'),














]