from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'tick_app/home.html')


def register_page(request):
    return render(request, 'tick_app/register.html')


def login_page(request):
    return render(request, 'tick_app/login.html')
