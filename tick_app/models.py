from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=200, null=True)
    serial_no = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, default='Active')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} | {self.serial_no}"


class Queue(models.Model):
    name = models.CharField(max_length=200, null=True)
    assigned_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    PRIORITY = (
        ('P1 (Critical)', 'P1 (Critical)'),
        ('P2 (High)', 'P2 (High)'),
        ('P3 (Medium)', 'P3 (Medium)'),
        ('P4 (Low)', 'P4 (Low)'),
        ('P5 (Info)', 'P5 (Info)'),
    )

    STATUS = (
        ('New', 'New'),
        ('Resolved', 'Resolved'),
        ('Abandoned', 'Abandoned'),
        ('Info required', 'Info required'),
        ('Updated', 'Updated'),
        ('Active', 'Active'),
    )

    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_engineer = models.CharField(max_length=100, blank=True)
    priority = models.CharField(max_length=16, choices=PRIORITY)
    short_desc = models.CharField(max_length=50)
    long_desc = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=16, choices=STATUS, default='New')

    def __str__(self):
        return self.short_desc


class Comment(models.Model):
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    ticket = models.ForeignKey(Ticket, null=True, on_delete=models.SET_NULL)
    # user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.comment
