from django.urls import path
from . import views


urlpatterns=[
path('', views.index, name='index'),
path('contact_us', views.contact_us, name='contact_us'),
path('technology', views.technology, name='technology'),













]