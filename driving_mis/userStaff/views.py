# Create your views here.
from django.shortcuts import render, redirect
from .models import Student,Payment
from django.db.models import Sum
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm   
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now 

@login_required
def dashboard_page(request):
    if request.user.is_superuser:
        return redirect('userStaff:dashboard')
    total_students = Student.objects.count()
    total_payments = Payment.objects.count()
    total_amount_today = Payment.objects.aggregate(
        total = Sum('amountPaid')
    )['total'] or 0

    recent_students = Student.objects.order_by('-enrollment_date')[:5]

    context = {
        'total_students': total_students,
        'total_payments': total_payments,
        'total_amount_today': total_amount_today,
        'recent_students' : recent_students, 
    }

    return render(request, "userStaff/staff_dashboard.html", context)

# STUDENTS
@login_required
def students_page(request):
    students = Student.objects.all()
    return render(request, "userStaff/students/staff_student_page.html", { 'students' : students})

@login_required
def student_add(request):
    if request.method == 'POST' :
        name = request.POST['name']
        phone  = request.POST['phone']
        address  = request.POST['address']
        course  = request.POST['course']
        enrollment_date  = request.POST['enrollment_date']
        total_fee  = request.POST['total_fee']
        fees_paid  = request.POST['fees_paid']
        notes = request.POST['notes']
        Student.objects.create(
            name = name,
            phone = phone,
            address = address,
            course = course,
            enrollment_date = enrollment_date,
            total_fee = total_fee,
            fees_paid = fees_paid,
            notes = notes,
        )
        messages.success(request,'Student Added!')
        return redirect('userStaff:staffStudents')
    return render(request, "userStaff/students/staff_student_add_page.html")

@login_required
def student_update(request, slug):
    student = Student.objects.get(slug=slug)
    if request.method == 'POST' :
        student.name = request.POST['name']
        student.phone  = request.POST['phone']
        student.address  = request.POST['address']
        student.course  = request.POST['course']
        student.enrollment_date  = request.POST['enrollment_date']
        student.total_fee  = request.POST['total_fee']
        student.fees_paid  = request.POST['fees_paid']
        student.notes = request.POST['notes']
        student.save()
        messages.info(request, "Student Record Updated!")
        return redirect('userStaff:staffStudents')
    else :
        return render(request, "userStaff/students/student_update_page.html", {"student" : student})

@login_required
def student_delete(request, slug):
    if request.method == 'POST' :
        student = Student.objects.get(slug=slug)
        student.delete()
        messages.error(request,"Student Deleted")
        return redirect('userStaff:staffStudents')
    return redirect('userAdmin:staffStudents')

# PAYMENTS
@login_required
def payments_page(request):
    payments = Payment.objects.all()
    return render(request, "userStaff/payments/staff_payment_page.html", {'payments' : payments})

@login_required
def payment_add(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_slug = request.POST['student']
        amount = request.POST['amountPaid']
        date = request.POST['paymentDate']
        method = request.POST['paymentMethod']
        student_obj = Student.objects.get(slug=student_slug)
        Payment.objects.create(
            student = student_obj,
            amountPaid = amount,
            paymentDate = date,
            paymentMethod = method,
        )
        messages.success(request,"Payment Recorded!")
        return redirect ('userStaff:staffPayments')
    return render(request, "userStaff/payments/staff_payment_add_page.html", {'students' : students })

@login_required
def payment_update(request, id):
    students = Student.objects.all()
    payment = Payment.objects.get(id=id)
    if request.method == 'POST' :
        payment.amountPaid = request.POST['amountPaid']
        payment.paymentDate = request.POST['paymentDate']
        payment.paymentMethod = request.POST['paymentMethod']
        payment.save()
        messages.info(request,'Payment Record Updated!')
        return redirect('userStaff:staffPayments')
    return render(request, "userStaff/payments/staff_payment_update_page.html", {"paymentData" : payment, 'students': students})

@login_required
def payment_delete(request, id):
    if request.method == 'POST' :
        payment = Payment.objects.get(id = id)
        payment.delete()
        messages.error(request, 'Payment Record Deleted!')
        return redirect('userStaff:staffPayments')
