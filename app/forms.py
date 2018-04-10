from django import forms
from django.forms import ModelForm
from .models import Person, Poll, Question, Choice


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Person
        fields = ('username', 'email', 'password')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Person
        fields = ('username', 'password')