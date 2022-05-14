from django import forms
from dashboard.models import Role, Nationality, Bank, Employee
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class AddEmployee(forms.ModelForm):
    employeeid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'please enter 5 characters eg. A0025'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'onchange': 'previewImage(this);'}))
    is_staff = forms.BooleanField(required=False)



    class Meta:
        model = Employee
        exclude = ['is_blocked', 'is_deleted', 'created', 'updated']


class AddBankAccount(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['employee', 'bank', 'bankAccountNum', 'salary']

class AddNationality(forms.ModelForm):
    class Meta:
        model = Nationality
        fields = ['country']
