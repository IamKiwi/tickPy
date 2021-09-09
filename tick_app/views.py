from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def home(request):
    return render(request, 'tick_app/home.html')


def register_page(request):
    return render(request, 'tick_app/register.html')


def login_page(request):
    return render(request, 'tick_app/login.html')


def create_new_ticket(request):
    resources = Resource.objects.all()

    context = {
        'resources': resources
    }

    return render(request, 'tick_app/new_ticket_form.html', context)


def customer_ticket_tracking(request):
    return render(request, 'tick_app/customer_ticket_tracking.html')


def admin_manage_resources(request):
    categories = Category.objects.all()
    resources = Resource.objects.all()
    categoryForm = CategoryForm()
    resourcesForm = ResourceForm()

    if request.method == "POST" and request.POST.get('serial_no') is None:
        print("Printing POST (category): ", request.POST)
        form = CategoryForm(request.POST)
        if form.is_valid():
            print(request.POST.get('category_name'))
            form.save()
            return redirect('admin_manage_resources')
    else:
        print("Printing POST (resource): ", request.POST)
        form = ResourceForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('admin_manage_resources')

    context = {
        'categories': categories,
        'resources': resources,
        'category_form': categoryForm,
        'resources_form': resourcesForm
    }

    return render(request, 'tick_app/admin_manage_resources.html', context)


def admin_manage_queues(request):
    return render(request, 'tick_app/admin_manage_queues.html')
