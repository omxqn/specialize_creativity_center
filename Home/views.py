from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'website_index.html')



def contact_us(request):
    return render(request, 'contact_us.html')


def technology(request):
    return render(request, 'technology.html')