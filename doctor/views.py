from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from Home.models import Profile
from authentication.utils import token_generator
from Home.decorators import allowed_users
from django.contrib.auth.decorators import login_required

from doctor.models import Appointment
from patient.models import Prescription, Medicines, Lab_examination, TestType
from pharamacy.models import Product


# Create your views here.

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])

def doctor_dashboard(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users,}
    return render(request,'doctor_dashboard.html',context)



@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])

def doctor_add_medicine(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        prescription_id = request.POST.get('prescription_id')
        medicine_name = request.POST.get('medicine_name')
        medicine_instruction = request.POST.get('medicine_instruction')
        dose_quantity = request.POST.get('dose_quantity')
        ps=Prescription.objects.get(id=prescription_id)
        product=Product.objects.get(id=medicine_name)
        Medicines.objects.create(prescription=ps,medicine_name=product.name,instruction=dose_quantity,medicine_formula=medicine_instruction,medicine_item=product
                                 ).save()
        return redirect('doctor_add_prescription',appointment_id)


def doctor_add_lab_test(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        prescription_id = request.POST.get('prescription_id')

        test_type = request.POST.get('test_type')
        x=TestType.objects.get(pk=test_type)
        instruction = request.POST.get('instruction')
        ps=Prescription.objects.get(id=prescription_id)
        Lab_examination.objects.create(prescription=ps,test_name=x.type_name,test_type_id=x.id,instruction=instruction,
                                 ).save()
        return redirect('doctor_add_prescription',appointment_id)

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])
def doctor_patients(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users,}
    return render(request,'doctor_patients.html',context)

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])
def doctor_appointments(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    my_appointments = Appointment.objects.filter(doctor=users).order_by('-created_at')

    items_per_page = 2

    paginator = Paginator(my_appointments, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    context = {'user_profile': user_profile,
               'users': users,'page_obj':page_obj}
    return render(request,'doctor_appointments.html',context)




@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])
def doctor_add_prescription(request,id):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    test_list = TestType.objects.all()
    appointment_info=Appointment.objects.get(id=id)
    if Prescription.objects.filter(doctor=appointment_info.doctor,patient=appointment_info.patient).exists():
        prescription_info = Prescription.objects.get(doctor=appointment_info.doctor,patient=appointment_info.patient)
        medicine_list = Medicines.objects.filter(prescription=prescription_info).order_by('-date')
        Lab_examination_list = Lab_examination.objects.filter(prescription=prescription_info).order_by('-date')
        products = Product.objects.all()

    else:


        prescription_info=Prescription.objects.create(doctor=appointment_info.doctor,patient=appointment_info.patient).save()
        medicine_list=Medicines.objects.filter(prescription=prescription_info).order_by('-date')
        Lab_examination_list=Lab_examination.objects.filter(prescription=prescription_info).order_by('-date')
        products = Product.objects.all()
    context = {'user_profile': user_profile,'test_list':test_list,
               'users': users,'appointment_info':appointment_info,'prescription_info':prescription_info,
               'medicine_list':medicine_list,'Lab_examination_list':Lab_examination_list,'products':products}
    return render(request,'doctor_prescription.html',context)
@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])
def doctor_delete_medicie(request,medicine_id,appoint_id):
    users = User.objects.get(username=request.user)


    x=Medicines.objects.get(id=medicine_id)
    x.delete()


    return redirect('doctor_add_prescription',appoint_id)
@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])
def doctor_delete_test(request,medicine_id,appoint_id):
    users = User.objects.get(username=request.user)


    x=Lab_examination.objects.get(id=medicine_id)
    x.delete()


    return redirect('doctor_add_prescription',appoint_id)





@login_required(login_url='Login')
@allowed_users(allowed_roles=['Doctor'])
def doctor_profile(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)

    context = {'user_profile': user_profile, 'users': users}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        phone = request.POST.get('phone_number')


        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname

        if len(phone) != 0:
            user_profile.phone = phone



        if len(request.FILES) != 0:
            my_file = request.FILES['upload']

            if my_file.content_type == 'image/jpg' or my_file.content_type == 'image/jpeg' or my_file.content_type == 'image/png':
                user_profile.picture = request.FILES['upload']

                users.save()
                user_profile.save()

                messages.success(request, 'Data updated successfully')
                return redirect('doctor_profile')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('doctor_profile')
        users.save()
        user_profile.save()
        messages.success(request, 'Data updated successfully')
        return redirect('doctor_profile')

    return render(request, 'doctors_settings.html', context)