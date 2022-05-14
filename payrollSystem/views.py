from django.shortcuts import render
from django.views.generic import TemplateView,UpdateView,CreateView,View
from django.contrib.auth.mixins import LoginRequiredMixin

from payrollSystem.forms import PayrollForm, PersonForm, RollForm, PayrollPersonForm, PersonScheduleForm
from .models import Payroll, Roll, Person
from .calender_models import PersonSchedule
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import reverse, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q

CURRENCY = settings.CURRENCY


# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'payrollSystem/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = PersonForm()
        context['create_roll'] = RollForm()
        context['persons'] = Person.objects.all()
        context['roll'] = Roll.objects.all()
        return context

@staff_member_required
def create_role_view(request):
    form = RollForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New Role added!')
    return redirect(reverse('payrollSystem:homepage'))

@staff_member_required
def create_person_view(request):
    form = PersonForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New Person added!')
    else:
        print('error')
        messages.warning(request, form.errors)
    return redirect(reverse('payrollSystem:homepage'))

@method_decorator(staff_member_required, name='dispatch')
class PersonCardView(UpdateView):
    model = Person
    template_name = 'payrollSystem/person_view.html'
    form_class = PersonForm

    def get_success_url(self):
        return reverse('payrollSystem:person_card', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = True
        context['page_title'] = self.object
        context['payment_form'] = PayrollPersonForm(initial={'person': self.object})
        context['calendar_form'] = PersonScheduleForm(initial={'person': self.object})
        context['payments'] = self.object.person_invoices.all()
        context['schedules'] = self.object.schedules.all()
        return context

    def form_valid(self, form):
        form.save()
        return super(PersonCardView, self).form_valid(form)


class RollUpdateView(UpdateView):
    template_name = 'payrollSystem/form.html'
    model = Roll
    form_class = RollForm

    def get_success_url(self):
        return reverse('payrollSystem:homepage')

    def get_context_data(self, **kwargs):
        context = super(RollUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Update {self.object}'
        context['back_url'] = reverse('payrollSystem:homepage')

        return context

    def form_valid(self, form):
        form.save()
        return super(RollUpdateView, self).form_valid(form)


@staff_member_required
def roll_delete_view(request, pk):
    obj = get_object_or_404(Roll, id=pk)
    obj.delete()
    return redirect(reverse('payrollSystem:homepage'))


# @method_decorator(staff_member_required, name='dispatch')
class PersonCardView(UpdateView):
    model = Person
    template_name = 'payrollSystem/person_view.html'
    form_class = PersonForm

    def get_success_url(self):
        return reverse('payrollSystem:person_card', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = True
        context['page_title'] = self.object
        context['payment_form'] = PayrollPersonForm(initial={'person': self.object})
        context['calendar_form'] = PersonScheduleForm(initial={'person': self.object})
        context['payments'] = self.object.person_invoices.all()
        context['schedules'] = self.object.schedules.all()
        return context

    def form_valid(self, form):
        form.save()
        return super(PersonCardView, self).form_valid(form)

@staff_member_required
def handle_payroll_view(request, pk, type_):
    if type_ == 'delete':
        obj = get_object_or_404(Payroll, id=pk)
        obj.delete()
    elif type_ == 'create':
        form = PayrollForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Payroll Added')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def handle_schedule_view(request, pk, type_):
    if type_ == 'delete':
        obj = get_object_or_404(PersonSchedule, id=pk)
        obj.delete()
    elif type_ == 'create':
        print('create')
        form = PersonScheduleForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            print('form valid')
            form.save()
            messages.success(request, 'New Payroll Added')
        else:
            print(form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_person_view(request, pk):
    person = get_object_or_404(Person, id=pk)
    person.delete()
    return redirect(reverse('payrollSystem:homepage'))

# class Attendance_New (LoginRequiredMixin,CreateView):
#     model = Attendance
#     form_class = AttendanceForm
#     login_url = 'account:login'
#     template_name = 'payrollSystem/create.html'
#     success_url = reverse_lazy('payrollSystem:attendance_new')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["today"] = timezone.localdate()
#         pstaff = Attendance.objects.filter(Q(status='PRESENT') & Q (date=timezone.localdate()))
#         context['present_staffers'] = pstaff
#         return context
#
# class Attendance_Out(LoginRequiredMixin,View):
#     login_url = 'account:login'
#
#     def get(self, request,*args, **kwargs):
#
#        user=Attendance.objects.get(Q(staff__id=self.kwargs['pk']) & Q(status='PRESENT')& Q(date=timezone.localdate()))
#        user.last_out=timezone.localtime()
#        user.save()
#        return redirect('payrollSystem:attendance_new')
