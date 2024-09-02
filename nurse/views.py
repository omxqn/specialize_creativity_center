from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import render, redirect


from Home.models import Profile
from Home.decorators import allowed_users
from django.contrib.auth.decorators import login_required

from patient.models import Lab_examination, Prescription, Medicines










@login_required(login_url='Login')
@allowed_users(allowed_roles=['nurse'])
def nurse_patient_prescription(request):
    users = User.objects.get(username=request.user)
    Prescriptions = Prescription.objects.all()

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'Prescriptions': Prescriptions}
    return render(request, 'nurse_patient_prescriptions.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['nurse'])
def nurse_prescription_details(request, id):
    users = User.objects.get(username=request.user)
    prescription_info = Prescription.objects.get(pk=id)
    medicine_list = Medicines.objects.filter(prescription=prescription_info).order_by('-date')
    Lab_examination_list = Lab_examination.objects.filter(prescription=prescription_info).order_by('-date')
    if request.method == 'POST':
        test_fee = request.POST.get('test_fee')
        examination_id = request.POST.get('examination_id')
        x = Lab_examination.objects.get(id=examination_id)

        if len(test_fee) != 0:
            x.test_fee = test_fee

        if len(request.FILES) != 0:
            my_file = request.FILES['test_upload']

            x.report = my_file

            x.save()

        x.save()

        messages.success(request, 'Report addedd successfully')
        return redirect('nurse_prescription_details', prescription_info.id)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'prescription_info': prescription_info, 'medicine_list': medicine_list,
               'Lab_examination_list': Lab_examination_list}
    return render(request, 'nurse_patient_prescriptions_details.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['nurse'])
def nurse_profile(request):
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
                return redirect('nurse_profile')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('nurse_profile')
        users.save()
        user_profile.save()
        messages.success(request, 'Data updated successfully')
        return redirect('nurse_profile')

    return render(request, 'nurse_setting.html', context)
