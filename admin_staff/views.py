from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
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
from patient.models import Patient


# Create your views here.

@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_dashboard(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, }
    return render(request, 'admin_site/dashboard_index.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def create_account(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, }

    if request.method == 'POST':

        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        Email = request.POST.get('Email')
        role = request.POST.get('role')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        ch = '@'

        strValue = Email.split(ch, 1)[0]

        username = strValue
        if not f_name:
            messages.error(request, 'First Name is required')
            return redirect('Sign_up')
        if not l_name:
            messages.error(request, 'Last Name is required')
            return redirect('Sign_up')
        if not Email:
            messages.error(request, 'Email is required')
            return redirect('Sign_up')

        if not Email:
            messages.error(request, 'Email is required')
            return redirect('Sign_up')
        if not phone_number:
            messages.error(request, 'Phone is required')
            return redirect('Sign_up')

        if gender == 'Select':
            messages.error(request, 'Please Select gender.')
            return redirect('Sign_up')

        try:
            if not User.objects.filter(email=Email).exists():
                x = User.objects.create_user(first_name=f_name, last_name=l_name, email=Email,
                                             username=username, password='xyz123!!')
                x.is_active = False

                y = Profile.objects.create(owner=x, gender=gender, phone=phone_number, role=role)
                # Fetch the group

                group = Group.objects.get(
                    name=role)  # replace 'admin_staff_member' with the name of the group you want to add the user to

                # Add the user to the group
                group.user_set.add(x)

                x.save()
                y.save()

                # generating account activation link and sending to user
                uidb64 = urlsafe_base64_encode(force_bytes(x.pk))
                domain = get_current_site(request).domain

                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(x)})
                activate_url = 'https://' + domain + link

                user_email = []
                user_email.append(Email)

                subject = 'Thank you for account creation with us.'

                html_content = render_to_string('email_template.html',
                                                {'first_name': x.first_name, 'last_name': x.last_name, 'role': role,
                                                 'activate_url': activate_url
                                                 })
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
                msg.attach_alternative(html_content, "text/html")
                # sending email
                msg.send()
                messages.info(request,
                              'Account Created Successfully. Please ask user to check his email to activate account.')
                return redirect('Sign_up')

            messages.info(request, 'User is already exist against this Email.')
            return redirect('Sign_up')
        except Exception as e:
            print('Exception while creation of signup', e)
            messages.info(request, 'Ops something happens unwanted.')
            return redirect('Sign_up')
    else:
        return render(request, 'admin_site/create_user.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def Setting(request):
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
                return redirect('Settings')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('Settings')
        users.save()
        user_profile.save()
        messages.success(request, 'Data updated successfully')
        return redirect('Settings')

    return render(request, 'admin_site/settings.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_patient_list_view(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    all_patients = Patient.objects.all().order_by('-created_at')
    context = {'user_profile': user_profile,
               'users': users, 'all_patients': all_patients}
    return render(request, 'admin_site/patients_list.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_doctor_list_view(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    all_doctors = Profile.objects.filter(role='Doctor').order_by('-created_at')
    context = {'user_profile': user_profile,
               'users': users, 'all_doctors': all_doctors}
    return render(request, 'admin_site/doctors_list.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_add_appointment(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    all_doctors = Profile.objects.filter(role='Doctor').order_by('-created_at')
    all_patient = Patient.objects.all().order_by('-created_at')
    if request.method == 'POST':
        select_doctor = request.POST.get('select-doctor')
        select_patient = request.POST.get('select-patient')
        appointment_on = request.POST.get('appointment_on')
        deposit_paid = request.POST.get('deposit_paid')
        fee_paid = request.POST.get('fee_paid')
        remarks = request.POST.get('remarks')

        if select_doctor == 'Select':
            messages.error(request, 'Select doctor please')
            return redirect('admin_add_appointment')
        if select_patient == 'Select':
            messages.error(request, 'Select patient please')
            return redirect('admin_add_appointment')
        if not appointment_on:
            messages.error(request, 'Appointment On is required')
            return redirect('admin_add_appointment')

        selected_doctor = User.objects.get(id=select_doctor)
        selected_patient = Patient.objects.get(id=select_patient)
        Appointment.objects.create(patient=selected_patient, doctor=selected_doctor, appointment_at=appointment_on,
                                   fee_paid=fee_paid, deposit_paid=deposit_paid, remarks=remarks,
                                   created_by=users.username).save()
        messages.success(request, 'Appointment scheduled succesfully.')

        return redirect('admin_patient_list_view')
    context = {'user_profile': user_profile,
               'users': users, 'all_doctors': all_doctors, 'all_patient': all_patient}

    return render(request, 'admin_site/add_appointment.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_edit_appointment(request, id):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    all_doctors = Profile.objects.filter(role='Doctor').order_by('-created_at')
    all_patient = Patient.objects.all().order_by('-created_at')
    appointment_info = Appointment.objects.get(id=id)
    if request.method == 'POST':
        select_doctor = request.POST.get('select-doctor')

        appointment_on = request.POST.get('appointment_on')
        deposit_paid = request.POST.get('deposit_paid')
        fee_paid = request.POST.get('fee_paid')
        remarks = request.POST.get('remarks')

        if len(appointment_on) != 0:
            appointment_info.appointment_at = appointment_on
            appointment_info.save()
        if len(deposit_paid) != 0:
            appointment_info.deposit_paid = deposit_paid
            appointment_info.save()
        if len(fee_paid) != 0:
            appointment_info.fee_paid = fee_paid
            appointment_info.save()
        if len(remarks) != 0:
            appointment_info.remarks = remarks
            appointment_info.save()

        if select_doctor != 'Select':
            selected_doctor = User.objects.get(id=select_doctor)
            appointment_info.doctor = selected_doctor
            appointment_info.save()

        appointment_info.save()

        messages.success(request, 'Appointment updated succesfully.')

        return redirect('admin_appointment_list_view')
    context = {'user_profile': user_profile,
               'users': users, 'all_doctors': all_doctors, 'all_patient': all_patient,
               'appointment_info': appointment_info}

    return render(request, 'admin_site/edit_appointment.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_appointment_list_view(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    all_appointments = Appointment.objects.all().order_by('-created_at')
    context = {'user_profile': user_profile,
               'users': users, 'all_appointments': all_appointments}
    return render(request, 'admin_site/appointment_list.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_doctor_detail_view(request, id):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    doctor_info = Profile.objects.get(id=id)
    context = {'user_profile': user_profile,
               'users': users, 'doctor_info': doctor_info}
    return render(request, 'admin_site/doctor_details.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_appointment_detail(request, id):
    users = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(owner=users)

    appointment_info = Appointment.objects.get(id=id)
    doctor_info = Profile.objects.get(id=id)
    context = {'user_profile': user_profile,
               'users': users, 'appointment_info': appointment_info}
    return render(request, 'admin_site/appointment_details.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_patient_detail(request, id):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    patient_info = Patient.objects.get(id=id)
    context = {'user_profile': user_profile,
               'users': users, 'patient_info': patient_info}
    return render(request, 'admin_site/patients_details.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_add_patient(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)

    context = {'user_profile': user_profile,
               'users': users}

    if request.method == 'POST':
        pname = request.POST.get('pname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        health_insurance = request.POST.get('health_insurance')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')

        if not pname:
            messages.error(request, 'Name is required')
            return redirect('admin_add_patient')
        if gender == 'Select':
            messages.error(request, 'Gender is required')
            return redirect('admin_add_patient')
        if not dob:
            messages.error(request, 'DOB is required')
            return redirect('admin_add_patient')
        if not health_insurance:
            messages.error(request, 'Health Insurance is required')

            return redirect('admin_add_patient')
        if not email:
            messages.error(request, 'Email is required')

            return redirect('admin_add_patient')
        if not phone_no:
            messages.error(request, 'Phone is required')

            return redirect('admin_add_patient')
        if not address:
            messages.error(request, 'Address is required')

            return redirect('admin_add_patient')
        Patient.objects.create(name=pname, gender=gender, DOB=dob, health_insurance=health_insurance,
                               email=email, phone=phone_no, address=address).save()
        messages.error(request, 'Patient added succesffuly.')

        return redirect('admin_patient_list_view')
    return render(request, 'admin_site/add_patient.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['admin_staff_member'])
def admin_edit_patient(request, id):
    users = User.objects.get(username=request.user)
    patient_info = Patient.objects.get(id=id)

    user_profile = Profile.objects.get(owner=users)

    context = {'user_profile': user_profile,
               'users': users, 'patient_info': patient_info}

    if request.method == 'POST':
        pname = request.POST.get('pname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        health_insurance = request.POST.get('health_insurance')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')

        if len(pname) != 0:
            patient_info.name = pname
            patient_info.save()
        if len(gender) != 0:
            patient_info.gender = gender
            patient_info.save()
        if len(dob) != 0:
            patient_info.DOB = dob
            patient_info.save()
        if len(health_insurance) != 0:
            patient_info.health_insurance = health_insurance
            patient_info.save()
        if len(email) != 0:
            patient_info.email = email
            patient_info.save()
        if len(phone_no) != 0:
            patient_info.phone = phone_no
            patient_info.save()
        if len(address) != 0:
            patient_info.address = address
            patient_info.save()

        patient_info.save()

        messages.error(request, 'Patient updated succesffuly.')

        return redirect('admin_patient_list_view')
    return render(request, 'admin_site/edit_patient.html', context)
