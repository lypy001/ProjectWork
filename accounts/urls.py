from django.urls import path
from accounts import views

app_name='accounts'
urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_user_view,name='register'),
    path('profile/view/', views.user_profile_view, name='userprofile'),
    path('change-password/', views.change_password, name='changepassword'),
]