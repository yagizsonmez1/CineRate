from django.shortcuts import render
from django.http import HttpResponse

def register(request):
    return HttpResponse("Register page coming soon.") # Just to avoid the breakdown of the site

def login(request):
    return HttpResponse("Login page coming soon") # Just to avoid the breakdown of the site


def home(request):
    return render(request, "movies/home.html")
