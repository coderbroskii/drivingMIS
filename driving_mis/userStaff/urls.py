from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'userStaff'

urlpatterns = [
    # path('', views.login_page, name='login'),
    path('/logout', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard_page, name='staffDashboard'),
    path('students/', views.students_page, name='staffStudents'),
    path('payments/', views.payments_page, name='staffPayments'),

    path('students/add/', views.student_add, name='StaffAddStudent'),
    path('students/update/<slug:slug>/', views.student_update, name='StaffUpdateStudent'),
    path('students/delete/<slug:slug>/', views.student_delete, name='StaffDeleteStudent'),

    path('payments/add/', views.payment_add, name='StaffAddPayment'),
    path('payments/update/<int:id>/', views.payment_update, name='StaffUpdatePayment'),
    path('payments/delete/<int:id>/', views.payment_delete, name='StaffDeletePayment'),

]