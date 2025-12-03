from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'userAdmin'

urlpatterns = [
    path('/logout', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('students/', views.students_page, name='students'),
    path('payments/', views.payments_page, name='payments'),
    path('staffs/', views.staffs_page, name='staffs'),

    path('students/add/', views.student_add, name='addStudent'),
    path('students/update/<slug:slug>/', views.student_update, name='updateStudent'),
    path('students/delete/<slug:slug>/', views.student_delete, name='deleteStudent'),

    path('payments/add/', views.payment_add, name='addPayment'),
    path('payments/update/<int:id>/', views.payment_update, name='updatePayment'),
    path('payments/delete/<int:id>/', views.payment_delete, name='deletePayment'),

    path('staffs/add/', views.staff_add, name='addStaff'),
    path('staffs/update/<int:staff_id>/', views.staff_update, name='updateStaff'),
    path('staffs/delete/<int:staff_id>/', views.staff_delete, name='deleteStaff'),
]