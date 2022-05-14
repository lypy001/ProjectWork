from django.urls import path
from .import views

app_name = 'leave'

urlpatterns = [
    path('apply/',views.leave_creation,name='applyleave'),
    path('pending/all/',views.leaves_list,name='pendingleaveslist'),
    path('approved/all/',views.leaves_approved_list,name='approvedleaveslist'),
    path('cancel/all/',views.cancel_leaves_list,name='canceleaveslist'),
    path('user_leave/view/<int:id>/',views.view_leaves,name='userleavedetails'),
    path('staff_leaves/table/',views.view_my_leave_table,name='staffleavetable'),
    path('approval/<int:id>/',views.approve_leave,name='userleaveapprove'),
    path('unapprove/<int:id>/',views.unapprove_leave,name='userleaveunapprove'),
    path('cancelled/<int:id>/',views.cancel_leave,name='userleavecancel'),
    path('uncancelled/<int:id>/',views.uncancel_leave,name='userleaveuncancel'),
    path('rejected/all/',views.leave_rejected_list,name='leavesrejected'),
    path('leave/reject/<int:id>/',views.reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',views.unreject_leave,name='unreject'),
]