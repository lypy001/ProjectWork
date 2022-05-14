from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from dashboard.managers import EmployeeManager
# Create your models here.
class Role(models.Model):
    # EmployeeRole
    role = models.CharField(max_length=125)
    roleDescription = models.CharField(max_length=125, null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name =_('Role')
        verbose_name_plural =_('Roles')
        ordering = 'role', 'created_at'

    def __str__(self):
        return self.role

class Nationality(models.Model):

    country = CountryField(blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name =_('Nationality')
        verbose_name_plural = _('Nationality')
        ordering = ['country', 'created_at']

    def __str__(self):
        return self.country

# class Religion(models.Model):
#     BUDDHISM = 'Buddhism'
#     NO_RELIGION = 'No Religion'
#     ISLAM = 'Islam'
#     CHRISTIAN = 'Christian'
#     TAOISM = 'Taoism'
#     CATHOLICISM ='Catholicism'
#     HINDUISM ='Hinduism'
#     SIKHISM = 'Sikhism'
#     OTHER = "Other"
#
#
#
#     RELIGION = [
#         (BUDDHISM, 'Buddhism'),
#         (NO_RELIGION, 'No Religion'),
#         (ISLAM, 'Islam'),
#         (CHRISTIAN, 'Christian'),
#         (TAOISM, 'Taoism'),
#         (CATHOLICISM, 'Catholicism'),
#         (HINDUISM, 'Hinduism'),
#         (SIKHISM, 'Sikhism'),
#         (OTHER, "Other")
#     ]
#
#     religion = models.CharField(max_length=125, null=True, blank=True)
#
#     created_at = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)
#
#     class Meta:
#         verbose_name = _('Religion')
#         verbose_name_plural = _('Religions')
#         ordering = ['religion', 'created_at']
#
#     def __str__(self):
#         return self.religion

class Bank(models.Model):
    # access table: employee.bank_set.


    employee = models.ForeignKey('Employee', help_text='select employee(s) to add bank account',
                                 on_delete=models.CASCADE, null=True, blank=False)
    bank = models.CharField(_('Name of Bank'), max_length=125, blank=False, null=True, help_text='')
    bankAccountNum = models.CharField(_('Account Number'), help_text='employee account number', max_length=30, blank=False,
                               null=True)
    salary = models.DecimalField(_('Starting Salary'), help_text='This is the initial salary of employee',
                                 max_digits=16, decimal_places=2, null=True, blank=False)

    created_at = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated'), auto_now=True, null=True)

    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')
        ordering = ['-bank','-bankAccountNum']


    def __str__(self):
        return self.bank

class Employee(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_KNOWN, 'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MISS = 'Miss'
    DR = 'Dr'


    TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MISS, 'Miss'),
        (DR, 'Dr'),

    )

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERN, 'Intern'),
    )

    SECONDARY = 'OLEVEL/NLevel'
    TERTIARY = 'Tertiary'
    PRIMARY = 'Primary Level'
    OTHER = 'Other'

    EDUCATIONAL_LEVEL = (

        (PRIMARY, 'Primary School'),
        (SECONDARY, 'OLevel'),
        (SECONDARY, 'NLevel'),
        (TERTIARY, 'Bachelor Degree'),
        (TERTIARY, 'Master Degree'),
        (TERTIARY, 'Doctoral(PhD) Degree'),
        (TERTIARY, 'Diploma'),
        (OTHER, 'Other')
    )

    BUDDHISM = 'Buddhism'
    NO_RELIGION = 'No Religion'
    ISLAM = 'Islam'
    CHRISTIAN = 'Christian'
    TAOISM = 'Taoism'
    CATHOLICISM = 'Catholicism'
    HINDUISM = 'Hinduism'
    SIKHISM = 'Sikhism'
    OTHER = "Other"

    RELIGION = [
        (BUDDHISM, 'Buddhism'),
        (NO_RELIGION, 'No Religion'),
        (ISLAM, 'Islam'),
        (CHRISTIAN, 'Christian'),
        (TAOISM, 'Taoism'),
        (CATHOLICISM, 'Catholicism'),
        (HINDUISM, 'Hinduism'),
        (SIKHISM, 'Sikhism'),
        (OTHER, "Other")
    ]

    # PERSONAL DATA
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField('Title', max_length=4, default=MR, choices=TITLE, blank=False, null=True)
    image = models.ImageField('Profile Image', upload_to='profiles', default='profiles/default.png', blank=True, null=True,help_text='upload image size less than 2.0MB')  # work on path username-date/image
    firstname = models.CharField('Firstname', max_length=125, null=False, blank=False)
    lastname = models.CharField('Lastname', max_length=125, null=False, blank=False)
    othername = models.CharField('Othername (optional)', max_length=125, null=True, blank=True)
    sex = models.CharField('Gender', max_length=10, default=MALE, choices=GENDER, blank=False)
    email = models.CharField('Email (optional)', max_length=255, default=None, blank=True, null=True)
    tel = PhoneNumberField(default='+06512345678', null=False, blank=False, verbose_name='Phone Number (Example +6512345678)',
                           help_text='Enter number with Country Code Eg. +065 1234 5678')
    dateOfBirth = models.DateField('Date of Birth', blank=False, null=False, help_text="Enter mm/dd/yy Eg. 10/25/99")
    religion = models.CharField('Religion',max_length =30, default=NO_RELIGION, choices=RELIGION,null=True,blank =False)
    nationality = CountryField(blank=True)
    address = models.CharField('Address', help_text='Enter address', max_length=125, null=True,blank=True)

    education = models.CharField('Education',help_text='highest educational standard ie. your last level of schooling',max_length=20, default=PRIMARY, choices=EDUCATIONAL_LEVEL, blank=False, null=True)

    # COMPANY DATA

    role = models.CharField('Role', help_text='Enter Role Of Employee',max_length= 125, null=True, default=None)
    startdate = models.DateField('Date of Employement ', help_text='Enter date of employement in mm/dd/yy Eg. 10/25/99"', blank=False, null=True)
    employeetype = models.CharField('Employee Type', max_length=15, default=FULL_TIME, choices=EMPLOYEETYPE,
                                    blank=False, null=True)
    employeeid = models.CharField('Employee ID Number', max_length=10, null=True, blank=True)


    # app related

    is_blocked = models.BooleanField('Is Blocked', help_text='button to toggle employee block and unblock',
                                     default=False)
    is_deleted = models.BooleanField('Is Deleted', help_text='button to toggle employee deleted and undelete',
                                     default=False)

    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True, null=True)

    # PLUG MANAGERS
    objects = EmployeeManager()

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname + ' ' + lastname
            return fullname
        elif othername:
            fullname = firstname + ' ' + lastname + ' ' + othername
            return fullname
        return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.dateOfBirth.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return

    @property
    def can_apply_leave(self):
        pass

    @property
    def get_birthdate(self):
        if self.dateOfBirth:
            return self.dateOfBirth.strftime('%A,%d %B')  # Thursday,04 May -> staffs age privacy
        return

    @property
    def birthday_today(self):
        '''
        returns True, if birthday is today else False
        '''
        return self.dateOfBirth.day == datetime.date.today().day

    @property
    def days_check_date_fade(self):
        '''
        Check if Birthday has already been celebrated ie in the Past     ie. 4th May  & today 8th May 4 < 8 -> past else present or future '''
        return self.dateOfBirth.day < datetime.date.today().day  # Assumption made,If that day is less than today day,in the past

    def birthday_counter(self):
        '''
        This method counts days to birthday -> 2 day's or 1 day
        '''
        today = datetime.date.today()
        current_year = today.year

        birthday = self.dateOfBirth  # eg. 5th May 1995

        future_date_of_birth = datetime.date(current_year, birthday.month,
                                             birthday.day)  # assuming born THIS YEAR ie. 5th May 2019

        if birthday:
            if (future_date_of_birth - today).days > 1:

                return str((future_date_of_birth - today).days) + ' day\'s'

            else:

                return ' tomorrow'

        return



