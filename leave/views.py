from django.shortcuts import render, redirect,get_object_or_404
from .forms import LeaveCreationForm
from django.contrib import messages
from .models import Leave
from dashboard.models import*


# Create your views here.
def leave_creation(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = LeaveCreationForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.user
            instance.user = user
            instance.save()

            # print(instance.defaultdays)
            messages.success(request, 'Leave Request Sent,wait for Human Resource Managers response',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('leave:applyleave')

        messages.error(request, 'failed to Request a Leave,please check entry dates',
                       extra_tags='alert alert-warning alert-dismissible show')
        return redirect('leave:applyleave')

    dataset = dict()
    form = LeaveCreationForm()
    dataset['form'] = form
    dataset['title'] = 'Apply for Leave'
    return render(request, 'leave/apply_leave.html', dataset)


def leaves_list(request):
    if not (request.user.is_staff and request.user.is_superuser):
        return redirect('/')
    leaves = Leave.objects.all_pending_leaves()
    return render(request, 'leave/leaves_pending_list.html', {'leave_list': leaves, 'title': 'leaves list - pending'})


def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    leaves = Leave.objects.all_approved_leaves()  # approved leaves -> calling model manager method
    return render(request, 'leave/leaves_approved.html', {'leave_list': leaves, 'title': 'approved leave list'})


def view_leaves(request, id):
    if not (request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user)[0]
    print(employee)
    return render(request, 'leave/leave_details.html', {'leave': leave, 'employee': employee,
                                                                'title': '{0}-{1} leave'.format(leave.user.username,
                                                                                                leave.status)})


def approve_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    user = leave.user
    employee = Employee.objects.filter(user=user)[0]
    leave.approve_leave

    messages.error(request, 'Leave successfully approved for {0}'.format(employee.get_full_name),
                   extra_tags='alert alert-success alert-dismissible show')
    return redirect('leave:userleavedetails', id=id)


def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leaves = Leave.objects.all_cancel_leaves()
    return render(request, 'leave/cancel_leave.html', {'leave_list_cancel': leaves, 'title': 'Cancel leave list'})


def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.unapprove_leave
    return redirect('leave:pendingleaveslist')  # redirect to unapproved list


def cancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.leaves_cancel

    messages.success(request, 'Leave is canceled', extra_tags='alert alert-success alert-dismissible show')
    return redirect('leave:canceleaveslist')  # work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave is uncanceled,now in pending list',
                     extra_tags='alert alert-success alert-dismissible show')
    return redirect('leave:canceleaveslist')  # work on redirecting to instance leave - detail view


def leave_rejected_list(request):
    dataset = dict()
    leave = Leave.objects.all_rejected_leaves()

    dataset['leave_list_rejected'] = leave
    return render(request, 'leave/rejected_leaves_list.html', dataset)


def reject_leave(request, id):
    dataset = dict()
    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave
    messages.success(request, 'Leave is rejected', extra_tags='alert alert-success alert-dismissible show')
    return redirect('leave:leavesrejected')


# return HttpResponse(id)


def unreject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave is now in pending list ', extra_tags='alert alert-success alert-dismissible show')

    return redirect('leave:leavesrejected')


# Rabotec staffs leaves table user only
def view_my_leave_table(request):
    # work on the logics
    if request.user.is_authenticated:
        user = request.user
        leaves = Leave.objects.filter(user=user)
        employee = Employee.objects.filter(user=user).first()
        print(leaves)
        dataset = dict()
        dataset['leave_list'] = leaves
        dataset['employee'] = employee
        dataset['title'] = 'Leaves List'
    else:
        return redirect('accounts:admin_login')
    return render(request, 'leave/staff_leaves_table.html', dataset)
