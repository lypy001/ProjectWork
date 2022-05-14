from django.contrib import admin
from django.urls import path
from .views import*



app_name = 'payrollSystem'
urlpatterns = [
    path('payroll/', HomepageView.as_view(), name='homepage'),
    path('create_person/', create_person_view, name='create'),
    path('create_roll/', create_role_view, name='create_roll'),
    path('update_roll/<int:pk>/', RollUpdateView.as_view(), name='update_roll'),
    path('delete_roll/<int:pk>/', roll_delete_view, name='delete_roll'),
    # path('attendance/in/', Attendance_New.as_view(), name='attendance_new'),
    # path('attendance/<int:pk>/out/', Attendance_Out.as_view(), name='attendance_out'),


    path('person-card/<int:pk>/', PersonCardView.as_view(), name='person_card'),
    path('person/create-payroll/<int:pk>/<slug:type_>/', handle_payroll_view, name='handle_payroll'),
    path('person/create-schedule/<int:pk>/<slug:type_>/', handle_schedule_view, name='handle_schedule'),

    path('person/delete/<int:pk>/', delete_person_view, name='person_delete')



]