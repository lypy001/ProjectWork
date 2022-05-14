from django.db import models
from .base_models import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from django.db.models import Sum, CASCADE
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

CURRENCY = settings.CURRENCY
PAYROLL_CHOICES = (
    ('1', 'Salary'),
    ('2', 'Extra'),
)

import datetime
from dateutil.relativedelta import relativedelta


class Roll(models.Model):
    active = models.BooleanField(default=True)
    roll = models.CharField(max_length=64)

    notes = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    objects = models.Manager()

    def __str__(self):
        return self.roll

    def save(self, *args, **kwargs):
        self.balance = self.person_set.all().aggregate(Sum('balance'))['balance__sum'] \
            if self.person_set.all().exists() else 0
        super().save(*args, *kwargs)

    def tag_balance(self):
        return '%s %s' % ( CURRENCY,self.balance)




class Person(models.Model):
    active = models.BooleanField(default=True),
    name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    # phone = models.CharField(max_length=10, blank=True)
    # phone1 = models.CharField(max_length=10, blank=True)
    roll = models.ForeignKey(Roll, null=True, blank=True, verbose_name='Roll',
                                   on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    value_per_hour = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    extra_per_hour = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    monthly_salary = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.balance = self.update_balance()
        super().save(*args, **kwargs)
        self.roll.save() if self.roll else ''

    def update_balance(self):
        queryset = self.person_invoices.all()
        value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.aggregate(Sum('paid_value'))['paid_value__sum'] if queryset else 0
        diff = value - paid_value
        return diff





    def tag_balance(self):
        return '%s %s' % ( CURRENCY, self.balance)

    def tag_occupation(self):
        return f'{self.roll.roll}' if self.roll else 'No data'

    def get_card_url(self):
        return reverse('payrollSystem:person_card', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('payrollSystem:person_delete', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        roll_name = request.GET.getlist('roll_name', None)
        queryset = queryset.filter(name__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(roll__id__in=roll_name) if roll_name else queryset

        return queryset


class PayrollInvoiceManager(models.Manager):
    def invoice_per_person(self, instance):
        return super(PayrollInvoiceManager, self).filter(person=instance)

    def not_paid(self):
        return super(PayrollInvoiceManager, self).filter(is_paid=False)


class Payroll(DefaultOrderModel):

    person = models.ForeignKey(Person, on_delete=CASCADE ,related_name='person_invoices')
    category = models.CharField(max_length=1, choices=PAYROLL_CHOICES, default='1')
    objects = models.Manager()

    class Meta:
        ordering = ['is_paid', '-date_expired', ]

    def __str__(self):
        return '%s' % (self.date_expired)

    def __str__(self):
        return '%s' % ( self.person.name)

    def save(self, *args, **kwargs):
        self.final_value = self.value
        self.paid_value = self.final_value if self.is_paid else 0
        # if self.id:
        #     self.title = f'Title {self.id}' if not self.title else self.title
        super(Payroll, self).save(*args, **kwargs)
        self.person.save()


# class Attendance(models.Model):
#     STATUS = (('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT'), ('UNAVAILABLE', 'UNAVAILABLE'))
#     date = models.DateField(auto_now_add=True)
#     first_in = models.TimeField()
#     last_out = models.TimeField(null=True)
#     status = models.CharField(choices=STATUS, max_length=15)
#     staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#
#     def save(self, *args, **kwargs):
#         self.first_in = timezone.localtime()
#         super(Attendance, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return 'Attendance -> ' + str(self.date) + ' -> ' + str(self.staff)