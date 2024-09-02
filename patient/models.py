from django.contrib.auth.models import User
from django.db import models

from pharamacy.models import Product


# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)

    gender = models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=2500,null=True,blank=True)
    health_insurance = models.CharField(max_length=2500,null=True,blank=True)
    created_at = models.DateField(auto_now=True, editable=True)
    DOB = models.DateField(null=True,blank=True)



class PatientCaseStudy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True)
    symptoms = models.CharField(max_length=2500,null=True,blank=True)
    diagnosis = models.CharField(max_length=2500,null=True,blank=True)
    blood_pressure = models.CharField(max_length=2500,null=True,blank=True)
    sugar = models.CharField(max_length=2500,null=True,blank=True)
    weight = models.CharField(max_length=2500,null=True,blank=True)
    height = models.CharField(max_length=2500,null=True,blank=True)
    is_diabetic = models.CharField(max_length=2500,null=True,blank=True)
    is_hyper_tension = models.CharField(max_length=2500,null=True,blank=True)
    treatment_plan = models.CharField(max_length=2500,null=True,blank=True)
    major_disease1 = models.CharField(max_length=2500,null=True,blank=True)
    major_disease2 = models.CharField(max_length=2500,null=True,blank=True)
    major_disease3 = models.CharField(max_length=2500,null=True,blank=True)
    major_disease4 = models.CharField(max_length=2500,null=True,blank=True)
    major_disease5 = models.CharField(max_length=2500,null=True,blank=True)
    any_desription = models.CharField(max_length=2500,null=True,blank=True)
    date = models.DateTimeField(auto_now=True, editable=True)

    doctor = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)



class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True)

    prescription_text = models.CharField(max_length=2500,null=True,blank=True)
    date_prescribed = models.DateTimeField(auto_now=True,editable=True)

    doctor = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class Medicines(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)

    medicine_name = models.CharField(max_length=2500, null=True, blank=True)
    medicine_type = models.CharField(max_length=2500, null=True, blank=True)
    medicine_formula = models.CharField(max_length=2500, null=True, blank=True)

    instruction = models.CharField(max_length=2500, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, editable=True)
    medicine_item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)


class Lab_examination(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)

    test_name = models.CharField(max_length=2500, null=True, blank=True)
    test_type = models.CharField(max_length=2500, null=True, blank=True)
    test_type_id = models.CharField(max_length=2500, null=True, blank=True)
    report = models.FileField(upload_to='Test_Reports', blank=True)


    instruction = models.CharField(max_length=2500, null=True, blank=True)
    test_fee = models.IntegerField( null=True, blank=True)
    date = models.DateTimeField(auto_now=True, editable=True)

    def lab_test_details(self):
        obj=TestType.objects.get(pk=self.test_type_id)
        return obj






class test_perameters(models.Model):


    perameter_name = models.CharField(max_length=2500, null=True, blank=True,verbose_name='Test Name')


    ref_range = models.CharField(max_length=2500, null=True, blank=True,verbose_name='Ref. Range')

    date = models.DateTimeField(auto_now=True, editable=True)
    def __str__(self):
        return self.perameter_name

class TestType(models.Model):
    type_name = models.CharField(max_length=1000, verbose_name='Test Type', null=True, blank=True)
    test_fee = models.IntegerField(null=True, blank=True, verbose_name='Fee')
    related_perameters = models.ManyToManyField(test_perameters, null=True, blank=True,verbose_name='Related Perameters')


    def __str__(self):
        return self.type_name


class Test(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)

    test_type = models.CharField(max_length=2500, null=True, blank=True, verbose_name='Test Type')
    perameter_name = models.CharField(max_length=2500, null=True, blank=True, verbose_name='Test Name')
    results = models.CharField(max_length=2500, null=True, blank=True, verbose_name='Results')

    ref_range = models.CharField(max_length=2500, null=True, blank=True, verbose_name='Ref. Range')

    date = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.test_type