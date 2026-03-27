from django.shortcuts import render, redirect
from .models import Student, Payment
from django.db.models import Sum
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm   
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now 

@login_required
def dashboard_page(request):
    if request.user.is_superuser:
        return redirect('userAdmin:dashboard')
    total_students = Student.objects.count()
    total_payments = Payment.objects.count()
    total_amount_today = Payment.objects.aggregate(
        total=Sum('amountPaid')
    )['total'] or 0

    recent_students = Student.objects.order_by('-enrollment_date')[:5]

    context = {
        'total_students': total_students,
        'total_payments': total_payments,
        'total_amount_today': total_amount_today,
        'recent_students': recent_students,
    }

    return render(request, "userStaff/staff_dashboard.html", context)

# STUDENTS
@login_required
def students_page(request):
    students = Student.objects.all()
    return render(request, "userStaff/students/staff_student_page.html", {'students': students})

@login_required
def student_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        course = request.POST['course']
        enrollment_date = request.POST['enrollment_date']
        total_fee = request.POST['total_fee']
        fees_paid = request.POST['fees_paid']
        notes = request.POST['notes']

        if not name.strip():
            messages.error(request, "Name cannot be empty")
            return redirect('userStaff:StaffAddStudent')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('userStaff:StaffAddStudent')
        

        if not total_fee.isdigit() or int(total_fee) <= 0:
            messages.error(request, "Total fee must be a positive number")
            return redirect('userStaff:StaffAddStudent')

        if not fees_paid.isdigit() or int(fees_paid) < 0:
            messages.error(request, "Fees paid cannot be negative")
            return redirect('userStaff:StaffAddStudent')

        if int(fees_paid) > int(total_fee):
            messages.error(request, "Fees paid cannot exceed total fee")
            return redirect('userStaff:StaffAddStudent')

        Student.objects.create(
            name=name,
            phone=phone,
            address=address,
            course=course,
            enrollment_date=enrollment_date,
            total_fee=total_fee,
            fees_paid=fees_paid,
            notes=notes,
        )
        messages.success(request, 'Student Added!')
        return redirect('userStaff:staffStudents')
    return render(request, "userStaff/students/staff_student_add_page.html")

@login_required
def student_update(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        course = request.POST['course']
        enrollment_date = request.POST['enrollment_date']
        total_fee = request.POST['total_fee']
        fees_paid = request.POST['fees_paid']
        notes = request.POST['notes']

        if not name.strip():
            messages.error(request, "Name cannot be empty")
            return redirect('userStaff:StaffUpdateStudent', id=id)

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('userStaff:StaffUpdateStudent', id=id)

        if not total_fee.isdigit() or int(total_fee) <= 0:
            messages.error(request, "Total fee must be positive")
            return redirect('userStaff:StaffUpdateStudent', id=id)

        if not fees_paid.isdigit() or int(fees_paid) < 0:
            messages.error(request, "Fees paid cannot be negative")
            return redirect('userStaff:StaffUpdateStudent', id=id)

        if int(fees_paid) > int(total_fee):
            messages.error(request, "Fees paid cannot exceed total fee")
            return redirect('userStaff:StaffUpdateStudent', id=id)

        student.name = name
        student.phone = phone
        student.address = address
        student.course = course
        student.enrollment_date = enrollment_date
        student.total_fee = total_fee
        student.fees_paid = fees_paid
        student.notes = notes
        student.save()
        messages.info(request, "Student Record Updated!")
        return redirect('userStaff:staffStudents')
    return render(request, "userStaff/students/staff_student_update_page.html", {"student": student})

@login_required
def student_delete(request, id):  # ← slug to id
    if request.method == 'POST':
        student = Student.objects.get(id=id)  # ← slug=slug to id=id before it was using slug now its id
        student.delete()
        messages.error(request, "Student Deleted")
        return redirect('userStaff:staffStudents')
    return redirect('userStaff:staffStudents')

# PAYMENTS
@login_required
def payments_page(request):
    payments = Payment.objects.all()
    return render(request, "userStaff/payments/staff_payment_page.html", {'payments': payments})

@login_required
def payment_add(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST['student']
        amount = int(request.POST['amountPaid'])
        date = request.POST['paymentDate']
        method = request.POST['paymentMethod']

        student_obj = Student.objects.get(id=student_id)  # ← slug to id
        if amount <= 0:
            messages.error(request, "Payment must be greater than zero")
        elif amount > student_obj.balance:
            messages.error(request, "Payment exceeds remaining balance")
        else:
            Payment.objects.create(
                student=student_obj,
                amountPaid=amount,
                paymentDate=date,
                paymentMethod=method,
            )
            messages.success(request, "Payment Recorded!")
        return redirect('userStaff:staffPayments')
    return render(request, "userStaff/payments/staff_payment_add_page.html", {'students': students})

@login_required
def payment_update(request, id):
    students = Student.objects.all()
    payment = Payment.objects.get(id=id)
    if request.method == 'POST':
        payment.amountPaid = request.POST['amountPaid']
        payment.paymentDate = request.POST['paymentDate']
        payment.paymentMethod = request.POST['paymentMethod']
        payment.save()
        messages.info(request, 'Payment Record Updated!')
        return redirect('userStaff:staffPayments')
    return render(request, "userStaff/payments/staff_payment_update_page.html", {"paymentData": payment, 'students': students})

@login_required
def payment_delete(request, id):
    if request.method == 'POST':
        payment = Payment.objects.get(id=id)
        payment.delete()
        messages.error(request, 'Payment Record Deleted!')
        return redirect('userStaff:staffPayments')