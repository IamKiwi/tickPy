from django import forms
from django.forms import ModelForm
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'})
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource Name'}),
            'serial_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'value': 'Active', 'hidden': True}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Queue Name'})
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"
        widgets = {
            'queue': forms.Select(attrs={'class': 'form-control'}),
            'resource': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'short_desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short description'}),
            'long_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': '5',
                                               'placeholder': 'Describe your problem...'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'value': 'New', 'hidden': True}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '2',
                                             'placeholder': 'Provide additional required information...'}),
        }
