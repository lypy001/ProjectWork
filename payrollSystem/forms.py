from django import forms
from .models import Person,Payroll, Roll
from .widget  import XDSoftDateTimePickerInput
from .calender_models import PersonSchedule
from bootstrap_datepicker_plus.widgets import  DateTimePickerInput
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PersonScheduleForm(BaseForm, forms.ModelForm):
    #
    # date_start = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=XDSoftDateTimePickerInput(), label='From..'
    #
    #
    # )
    #
    # date_end = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=XDSoftDateTimePickerInput(), label='Until...'
    #
    # )
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Date')

    person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = PersonSchedule
        fields = ['date','hours', 'person', 'category']




class PayrollForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Date')
    class Meta:
        model = Payroll
        fields = ['is_paid', 'date_expired', 'person', 'category', 'value', 'notes', ]


class PersonForm(BaseForm, forms.ModelForm):
    active = forms.BooleanField(required=False)

    class Meta:
        model = Person
        fields = [ 'active','name', 'roll','value_per_hour', 'extra_per_hour','monthly_salary'
                  ]


class PayrollPersonForm(PayrollForm):
    person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.HiddenInput())


class RollForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Roll
        fields = ("roll",)

# class AttendanceForm(forms.ModelForm):
#     status = forms.ChoiceField(choices=Attendance.STATUS,widget=forms.Select(attrs={'class':'form-control w-50'}))
#     staff = forms.ModelChoiceField(User.objects.filter(Q(attendance__status=None) | ~Q(attendance__date = timezone.localdate())), widget=forms.Select(attrs={'class':'form-control w-50'}))
#     class Meta:
#         model = Attendance
#         fields = ['status','staff']