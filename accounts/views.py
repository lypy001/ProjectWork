from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserLogin, AddUser
from dashboard.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse


# Create your views here.
def login_view(request):
    login_user = request.user
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                if login_user.is_authenticated:
                    return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Account is invalid', extra_tags='alert alert-error alert-dismissible show')
                return redirect('accounts:login')

        else:
            return HttpResponse('data not valid')

    dataset = dict()
    form = UserLogin()

    dataset['form'] = form
    return render(request, 'accounts/login.html', dataset)


def admin_login(request):
    login_user = request.user
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                if login_user.is_authenticated and request.user.is_superuser:
                    return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Account is invalid, user not an admin.',
                               extra_tags='alert alert-error alert-dismissible show')
                return redirect('accounts:admin_login')

        else:
            return HttpResponse('data not valid')

    dataset = dict()
    form = UserLogin()

    dataset['form'] = form
    return render(request, 'accounts/admin_login.html', dataset)


def employee_login(request):
    login_user = request.user
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
            if login_user.is_authenticated:
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Account is invalid, user not an employee.',
                               extra_tags='alert alert-error alert-dismissible show')
                return redirect('accounts:employee_login')

        else:
            return HttpResponse('data not valid')

    dataset = dict()
    form = UserLogin()

    dataset['form'] = form
    return render(request, 'accounts/employee_login.html', dataset)


def logout_view(request):
    logout(request)
    return redirect('Home')


def register_user_view(request):
    if request.method == 'POST':
        form = AddUser(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_staff = True
            instance.save()
            username = form.cleaned_data.get("username")

            messages.success(request, 'Account created for {0}.'.format(username),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('accounts:register')
        else:
            messages.error(request, 'Username or password is invalid',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('accounts:register')

    form = AddUser()
    dataset = dict()
    dataset['form'] = form
    dataset['title'] = 'register users'
    return render(request, 'accounts/register.html', dataset)


def user_profile_view(request):
    '''
	user profile view -> staffs (No edit) only admin/HR can edit.
	'''
    user = request.user
    if user.is_authenticated:
        employee = Employee.objects.filter(user=user).first()
        # bank = Bank.objects.filter(employee=employee).first()
        # role = Role.objects.filter(employee=employee).first()

        dataset = dict()
        dataset['employee'] = employee
        # dataset['bank'] = bank
        # dataset['role'] = role
        context = {'employee': employee}

        return render(request, 'accounts/view_profile.html', context)
    return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/')
    '''
    Please work on me -> success & error messages & style templates
    '''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('accounts:changepassword')
        else:
            messages.error(request, 'Error,changing password', extra_tags='alert alert-warning alert-dismissible show')
            return redirect('accounts:changepassword')

    form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
