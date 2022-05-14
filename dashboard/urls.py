from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path('welcome/',views.dashboard,name='dashboard'),
    path('employees/all/',views.dashboard_employees,name='employees'),
    path('employee/create/',views.dashboard_add_employees,name='addemployee'),
    path('employee/profile/<int:id>/',views.dashboard_employee_info,name='employeeinfo'),
    path('employee/profile/edit/<int:id>/',views.employee_edit_profile,name='edit'),

    path('bank/create/', views.dashboard_add_bank_details, name='bankaccountcreate'),
    path('bank/edit/<int:id>/',views.employee_edit_bank_details,name='bankedit'),
]