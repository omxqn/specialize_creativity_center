import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from django.urls import reverse
from django.views import View

from django.conf import settings


# Create your views here.
from django.contrib import auth,messages
import http.client

from django.conf import settings

from .utils import token_generator
from .models import *
# from Home.models import *
from django.core.mail import send_mail, EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from  django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from Home.models import *

#use to send OTP email to registered User vai gmail
def send_email_otp(x,user_email,otp):


    subject = 'Verification Code'

    html_content = render_to_string('otp_email_template.html',
                                    {'first_name': x.owner.first_name, 'last_name': x.owner.last_name,'otp':otp
                                     })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return None

#Login
def Login(request):
    if request.method == 'POST':
        Username = request.POST.get('username')
        Password = request.POST.get('password')
        print('Username and password is',Username,Password)
        if not Username:
            messages.error(request, 'Email is required')
            return redirect('Login')
        if not Password:
            messages.error(request, 'Password is required')
            return redirect('Login')
        #Checkingn User exist or not
        x = User.objects.filter(email=Username).first()




        if x is None:
            messages.error(request, 'No User found with this Email')
            return render(request, 'Login.html')
        #authenticating username and password
        user = auth.authenticate(username=Username.split('@', 1)[0], password=Password)
        print('Line no 71 from login:',user)

        if user is not None:
            if user.is_active:



                login(request, user)
                profile=Profile.objects.get(owner=x)
                if profile.role == 'Doctor':
                    return redirect('doctor_dashboard')
                if profile.role == 'admin_staff_member':
                    return redirect('admin_dashboard')
                if profile.role == 'nurse':
                    return redirect('nurse_patient_prescription')



                if profile.role == 'Pharamacy' or profile.role == 'Lab':
                    return redirect('pharamacy_dashboard')




            else:
                messages.error(request, 'Account is not activated')
                return redirect('Login')
        else:
            messages.warning(request, 'Invalid ID or password')
            return redirect('Login')



    return render(request, 'Login.html')

# from django.db import connection
#
# def Login(request):
#     # Get a cursor from the database connection
#     with connection.cursor() as cursor:
#         # Execute a query to get all table names
#         cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name ILIKE '%usdt' OR table_name ILIKE '%usd';")
#
#         # Fetch all table names
#         table_names = cursor.fetchall()
#
#         # Loop through the table names and execute DROP TABLE queries
#         for table_name in table_names:
#             cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]} CASCADE;")
#
#     return HttpResponse("Tables deleted successfully.")








def Logout(request):
    logout(request)
    messages.info(request,'You have been Logged Out')
    return redirect('Login')



#use to recover password
def forget_password(request):
    if request.method == 'POST':
        Username = request.POST.get('un')
        if not Username:
            messages.error(request, 'Email is required')
            return redirect('forget_password')

        user=User.objects.filter(email=Username).first()


        x= Profile.objects.filter(owner=user).first()
        if user is None:
            messages.error(request,'User not found with this Email')
            return render(request, 'forget-password.html')

        otp = str(random.randint(1000, 9999))
        x.otp = otp
        x.save()


        user_email = []
        user_email.append(user.email)
        send_email_otp(x, user_email, otp)


        request.session['Username'] = Username

        return redirect('reset_password')

    return render(request,'forget-password.html')


def reset_password(request):

    Username = request.session['Username']


    if request.method == 'POST':
        otp = request.POST.get('otp_number')



        print('Line no 249 OTP',otp)
        profile = Profile.objects.filter(owner__email=Username).first()

        if otp == profile.otp:

             request.session['Username'] = Username
             messages.success(request, 'Verification code match successfully')
             return redirect('update_password')

        else:
            messages.error(request,'Invalid OTP,please try again')
            return render(request, 'reset_password_otp.html')

    return render(request, 'reset_password_otp.html')


def update_password(request):
    Username = request.session['Username']


    if request.method == 'POST':
        users = User.objects.get(email=Username)
        user_profile = Profile.objects.get(owner=users)

        new_password = request.POST.get('new_password')



        if len(new_password)!=0:
            users.set_password(new_password)
            user_profile.changed_default_password = 'Yes'
            user_profile.save()
            users.save()

            messages.info(request, 'Password updated successfully,Please Login with New Set Password')
            return redirect('Login')

    else:

     return render(request,'update_password.html')



class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'Account Activated Successfully')
                return redirect('Login')

            else:
                messages.success(request, 'Account is already Activated')
                return redirect('Login')

        except Exception as e:
            pass
        return redirect('Login')