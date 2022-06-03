from django.http import HttpResponse
from django.shortcuts import render
from hackapp.dash_apps import helloworld
from hackapp.dash_apps import activity


# Create your views here.
def blank(request):
    return render(request, 'index.html')

def activity(request):
    return render(request, 'activity.html')