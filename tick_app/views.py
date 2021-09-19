from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def home(request):
    tickets = Ticket.objects.all()
    total_tickets = tickets.count()

    context = {
        'total_tickets': total_tickets
    }

    return render(request, 'tick_app/home.html', context)


def register_page(request):
    return render(request, 'tick_app/register.html')


def login_page(request):
    return render(request, 'tick_app/login.html')


def create_new_ticket(request):
    resources = Resource.objects.all()
    queues = Queue.objects.all()
    ticketForm = TicketForm()

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
        'ticket_form': ticketForm
    }

    return render(request, 'tick_app/new_ticket_form.html', context)


def abandon_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)

    ticket.status = 'Abandoned'
    ticket = Ticket.save(ticket, update_fields=['status'])

    return redirect('/show_ticket/'+pk)


def resolve_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)

    ticket.status = 'Resolved'
    ticket = Ticket.save(ticket, update_fields=['status'])

    return redirect('/show_ticket/'+pk)


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
        print(request.POST)
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('/show_ticket/'+pk)

    context = {
        'ticket': ticket,
        'ticket_comments': comments,
        'ticket_form': ticketForm,
        'comment_form': commentForm
    }

    return render(request, 'tick_app/show_ticket.html', context)


def add_comment_to_ticket(request, pk):
    form = CommentForm(request.POST)
    print("Printing POST (comment): ", request.POST)

    if form.is_valid():
        form.save()
        return redirect('/show_ticket/'+pk)


def customer_ticket_tracking(request):
    tickets = Ticket.objects.all()

    context = {'tickets': tickets}

    return render(request, 'tick_app/customer_ticket_tracking.html', context)


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


def admin_manage_users(request):
    context = {}

    return render(request, 'tick_app/admin_manage_users.html', context)


def admin_decom_resource(request, pk):
    resource = Resource.objects.get(id=pk)

    if request.method == "GET":
        print(request.GET)
        resource.status = 'DECOMMISIONED'
        resource.save()
        return redirect('admin_manage_resources')
