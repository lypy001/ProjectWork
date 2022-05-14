from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class AddUser(UserCreationForm):

    email = forms.EmailField()


    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2']



class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))