from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=200, null=True)
    serial_no = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Queue(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
