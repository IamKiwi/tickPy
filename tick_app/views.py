# Create your views here.

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from .template import *


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'User successfully registered. Please log in!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'tick_app/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'tick_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def home(request):
    group = request.user.groups.get()
    print(group)

    total_opened_tickets = 0
    total_resolved_tickets = 0
    total_new_tickets = 0
    total_in_progress = 0

    tickets = Ticket.objects.all()
    total_opened_tickets = tickets.count()
    total_resolved_tickets = tickets.filter(status="Resolved").count()
    total_new_tickets = tickets.filter(status="New").count()



    context = {
        'total_opened_tickets': total_opened_tickets,
        'total_resolved_tickets': total_resolved_tickets,
        'total_new_tickets': total_new_tickets,
        'total_in_progress': total_in_progress
    }

    return render(request, 'tick_app/home.html', context)


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def create_new_ticket(request):
    resources = Resource.objects.filter(status="Active")
    queues = Queue.objects.all()
    ticketForm = TicketForm()
    current_user = request.user

    if request.method == "POST":
        print(request.POST)
        form = TicketForm(request.POST)
        if form.is_valid():
            print("Data from Ticket Form")
            print(request.POST)
            form.save()
            return redirect('track_my_tickets')
        else:
            print("Coś się wyjebało i sobie ten głupi ryj rozwaliło : )")

    context = {
        'resources': resources,
        'queues': queues,
        'ticket_form': ticketForm,
        'current_user': current_user
    }

    return render(request, 'tick_app/new_ticket_form.html', context)


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def show_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    comments = ticket.comment_set.order_by('-id')
    ticketForm = TicketForm(instance=ticket)
    commentForm = CommentForm()

    if ticket.status == 'Resolved' or ticket.status == 'Abandoned':
        ticketForm.fields['queue'].widget.attrs['disabled'] = True
        ticketForm.fields['priority'].widget.attrs['disabled'] = True
        ticketForm.fields['resource'].widget.attrs['disabled'] = True
        ticketForm.fields['short_desc'].widget.attrs['disabled'] = True
        ticketForm.fields['long_desc'].widget.attrs['disabled'] = True

    if request.method == "POST":
        print('We will be updating ticket : )')
        print(request.POST)
        print(ticket)

        details = ""

        print(f"{request.POST.get('priority')} -> {ticket.priority}")
        print(f"{request.POST.get('queue')} -> {ticket.queue.id}")
        print(f"{request.POST.get('resource')} -> {ticket.resource.id}")
        print(f"{request.POST.get('short_desc')} -> {ticket.short_desc}")
        print(f"{request.POST.get('long_desc')} -> {ticket.long_desc}")

        if request.POST.get('priority') != ticket.priority:
            details += f"Priority changed from {ticket.priority} to {request.POST.get('priority')}\n"

        if int(request.POST.get('queue')) != ticket.queue.id:
            details += f"Queue changed from {Ticket.objects.get(id=pk).queue} to {ticket.queue}\n"

        if int(request.POST.get('resource')) != ticket.resource.id:
            details += f"Resource changed from {Ticket.objects.get(id=pk).resource} to {ticket.resource}\n"

        if request.POST.get('short_desc') != ticket.short_desc:
            details += f"Short description changed from {ticket.short_desc} to {request.POST.get('short_desc')}\n"

        if request.POST.get('long_desc') != ticket.long_desc:
            details += f"Long description changed from {ticket.long_desc} to {request.POST.get('long_desc')}\n"

        if details != "":
            comment = Comment.objects.create(**{'comment': details, 'ticket': ticket})

        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()

            ticket.status = 'Updated'
            ticket = Ticket.save(ticket, update_fields=['status'])

            return redirect('/show_ticket/' + pk)

    context = {
        'ticket': ticket,
        'ticket_comments': comments,
        'ticket_form': ticketForm,
        'comment_form': commentForm
    }

    return render(request, 'tick_app/show_ticket.html', context)


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def assign_ticket(request, pk):
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name

    working_engineer = f"{user_first_name} {user_last_name}"

    if request.method == "GET":
        ticket = Ticket.objects.get(id=pk)
        ticket.status = 'Active'
        ticket.assigned_engineer = working_engineer
        ticket = Ticket.save(ticket, update_fields=['assigned_engineer', 'status'])
        return redirect('/show_ticket/' + pk)


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def handle_comment(request, pk, status):
    ticket = Ticket.objects.get(id=pk)

    form = CommentForm(request.POST)
    print("Printing POST (comment): ", request.POST)

    if form.is_valid():
        form.save()
        ticket.status = status
        ticket = Ticket.save(ticket, update_fields=['status'])


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def add_comment_to_ticket(request, pk):
    handle_comment(request, pk, 'Info required')
    return redirect('/show_ticket/' + pk)


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def abandon_ticket(request, pk):
    handle_comment(request, pk, 'Abandoned')
    return redirect('/show_ticket/' + pk)


@allowed_users(allowed_roles=['admin', 'engineer'])
@login_required(login_url='login')
def resolve_ticket(request, pk):
    handle_comment(request, pk, 'Resolved')
    return redirect('/show_ticket/' + pk)


@allowed_users(allowed_roles=['admin', 'engineer', 'customer'])
@login_required(login_url='login')
def customer_ticket_tracking(request):
    tickets = request.user.ticket_set.order_by('-id')

    context = {'tickets': tickets}

    return render(request, 'tick_app/customer_ticket_tracking.html', context)


@allowed_users(allowed_roles=['admin', 'engineer'])
@login_required(login_url='login')
def engineer_queue_tracking(request):
    user_queues = request.user.queue_set.all()

    my_queues = []

    for i in user_queues:
        my_qu = Queue.objects.get(id=i.id)
        my_queues.append(my_qu.ticket_set.all())

    print(my_queues)

    context = {"my_tickets": my_queues}

    return render(request, 'tick_app/engineer_queue_tracking.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
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


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def admin_manage_queues(request):
    queues = Queue.objects.all()
    queueForm = QueueForm()

    if request.method == "POST":
        print("Printing POST (queue): ", request.POST)
        form = QueueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_queues')

    context = {
        'queues': queues,
        'queue_form': queueForm
    }

    return render(request, 'tick_app/admin_manage_queues.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def admin_manage_users(request):
    users = User.objects.all()

    context = {"users": users}
    return render(request, 'tick_app/admin_manage_users.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def admin_decom_resource(request, pk):
    resource = Resource.objects.get(id=pk)

    if request.method == "GET":
        print(request.GET)
        resource.status = 'DECOMMISIONED'
        resource.save()
        return redirect('admin_manage_resources')
