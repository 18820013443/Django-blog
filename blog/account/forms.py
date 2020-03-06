from django import forms
from django.shortcuts import render


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
 
