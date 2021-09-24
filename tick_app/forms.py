from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import PasswordInput
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
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Queue Name'}),
        }

        assigned_users = forms.ModelMultipleChoiceField(
            queryset=User.objects.filter(groups=2),
            widget=forms.CheckboxSelectMultiple()
        )


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"
        widgets = {
            'queue': forms.Select(attrs={'class': 'form-control'}),
            'resource': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_engineer': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
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
            'user': forms.TextInput(attrs={'class': 'form-control'})
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email address'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                    'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                    'placeholder': 'Confirm Password'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'})
        }
