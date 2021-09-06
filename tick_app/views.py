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
    return render(request, 'tick_app/new_ticket_form.html')


def customer_ticket_tracking(request):
    return render(request, 'tick_app/customer_ticket_tracking.html')


def admin_manage_resources(request):
    categories = Category.objects.all()
    categoryForm = CategoryForm()
    if request.method == "POST":
        print("Printing POST (amr): ", request.POST)
        form = CategoryForm(request.POST)
        if form.is_valid():
            print('OKOKOKOKOKOKOK')
            print(request.POST.get('category_name'))
            form.save()
            return redirect('admin_manage_resources')

    context = {'categories': categories, 'form': categoryForm}
    return render(request, 'tick_app/admin_manage_resources.html', context)


