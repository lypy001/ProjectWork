from django.shortcuts import render, redirect, get_object_or_404
from . import views
from dashboard.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from dashboard.forms import AddEmployee, AddBankAccount
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

app_name = 'dashboard'


# Create your views here.
def dashboard(request):
    dataset = dict()
    user = request.user
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    employees = Employee.objects.all()
    dataset['employees'] = employees

    return render(request, 'dashboard/dashboard_index.html')


def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()

    employees = Employee.objects.all()

    # pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    dataset['employee_list'] = employees_paginated

    dataset['all_employees'] = Employee.objects.all_employees()

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees list view'
    return render(request, 'dashboard/employee_app.html', dataset)


def dashboard_add_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = AddEmployee(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')
            instance.dateOfBirth = request.POST.get('dateOfBirth')
            instance.religion = request.POST.get('religion')
            instance.nationality = request.POST.get('nationality')


            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')
            instance.role = request.POST.get('role')


            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')


            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()


            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Trying to create dublicate employees with a single user account ',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:addemployee')

    dataset = dict()
    form = AddEmployee()
    dataset['form'] = form
    dataset['title'] = 'register employee'
    return render(request, 'dashboard/employee_add.html', dataset)


def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    bank_instance = Bank.objects.filter(employee=employee).first()

    dataset = dict()
    dataset['employee'] = employee
    dataset['bank'] = bank_instance
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_profile.html', dataset)


def employee_edit_profile(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = AddEmployee(request.POST or None, request.FILES or None, instance =employee)
        if form.is_valid():
            instance = form.save(commit=False)

            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')

            instance.birthday = request.POST.get('dateOfBirth')
            instance.religion = request.POST.get('religion')
            instance.nationality = request.POST.get('nationality')


            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')

            instance.role = request.POST.get('role')

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()
            messages.success(request, 'Account Updated Successfully !!!',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')

        else:

            messages.error(request, 'Error Updating account', extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = AddEmployee(request.POST or None, request.FILES or None, instance=employee)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_add.html', dataset )


def dashboard_add_bank_details(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = AddBankAccount(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee, id=employee_id)

            instance.employee = employee_object
            instance.name = request.POST.get('name')

            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Account Successfully Created for {0}'.format(employee_object.get_full_name),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')
        else:
            messages.error(request, 'Error Creating Account for {0}'.format(employee_object.get_full_name),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')

    dataset = dict()

    form = AddBankAccount()

    dataset['form'] = form
    dataset['title'] = 'Account Creation Form'
    return render(request, 'dashboard/add_bank_details.html', dataset)


def employee_edit_bank_details(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    bank_instance_obj = get_object_or_404(Bank, id=id)
    employee = bank_instance_obj.employee

    if request.method == 'POST':
        form = AddBankAccount(request.POST, instance=bank_instance_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = employee

            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Account Successfully Edited for {0}'.format(employee.get_full_name),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')
        else:
            messages.error(request, 'Error Updating Account for {0}'.format(employee.get_full_name),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')

    dataset = dict()

    form = AddBankAccount(request.POST or None, instance=bank_instance_obj)

    dataset['form'] = form
    dataset['title'] = 'Update Bank Account'

    return render(request, 'dashboard/add_bank_details.html', dataset)

def employee_dashboard_view(request,id):
    if request.user.is_authenticated:
        employee = Employee.objects.all()
    return render(request,'dashboard/dashboard_index.html', context={'employee':employee})

