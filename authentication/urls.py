from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views
from authentication.views import  VerificationView

urlpatterns=[





#Login
path('', views.Login, name='Login'),
#Logout
path('Logout',views.Logout,name='Logout'),
#Login Otp
#path('login-otp', views.login_otp , name="login_otp"),
#Forgot Password
path('forget_password', views.forget_password , name="forget_password"),
#Recover Password
path('reset_password', views.reset_password , name="reset_password"),
path('update_password', views.update_password , name="update_password"),

#url to activate the account
path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),








]