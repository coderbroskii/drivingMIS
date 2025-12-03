from django.shortcuts import render, redirect
from .models import Student,Payment,Staff
from django.db.models import Sum  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now 

@login_required
def dashboard_page(request):
    if not request.user.is_superuser:
        return redirect('userStaff:staffDashboard')
    total_students = Student.objects.count()
    total_payments = Payment.objects.count()
    total_staffs= Staff.objects.count()
    total_amount = Payment.objects.aggregate(
        total = Sum('amountPaid')
    )['total'] or 0

    recent_students = Student.objects.order_by('-enrollment_date')[:5]

    context = {
        'total_students': total_students,
        'total_staffs': total_staffs,
        'total_payments': total_payments,
        'total_amount': total_amount,
        'recent_students' : recent_students, 
    }

    return render(request, "userAdmin/dashboard_page.html", context)

# STUDENTS
@login_required
def students_page(request):
    students = Student.objects.all()
    return render(request, "userAdmin/students/student_page.html", { 'students' : students})

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
        return redirect('userAdmin:students')
    return render(request, "userAdmin/students/student_add_page.html")

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
        return redirect('userAdmin:students')
    else :
        return render(request, "userAdmin/students/student_update_page.html", {"student" : student})

@login_required
def student_delete(request, slug):
    if request.method == 'POST' :
        student = Student.objects.get(slug=slug)
        student.delete()
        messages.error(request,"Student Deleted")
        return redirect('userAdmin:students')
    return redirect('userAdmin:students')

# PAYMENTS
@login_required
def payments_page(request):
    payments = Payment.objects.all()
    return render(request, "userAdmin/payments/payment_page.html", {'payments' : payments})

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
        return redirect ('userAdmin:payments')
    return render(request, "userAdmin/payments/payment_add_page.html", {'students' : students })

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
        return redirect('userAdmin:payments')
    return render(request, "userAdmin/payments/payment_update_page.html", {"paymentData" : payment, 'students': students})

@login_required
def payment_delete(request, id):
    if request.method == 'POST' :
        payment = Payment.objects.get(id = id)
        payment.delete()
        messages.error(request, 'Payment Record Deleted!')
        return redirect('userAdmin:payments')


# STAFFS
@login_required
def staffs_page(request):
    staffs = Staff.objects.all()
    return render(request, "userAdmin/staffs/staff_page.html", {'staffs': staffs})

@login_required
def staff_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        Staff.objects.create(
            name = name,
            phone = phone,
            email = email,
        )
        messages.success(request,'Staff Added!')
        return redirect ('userAdmin:staffs')
    return render(request, "userAdmin/staffs/staff_add_page.html")

@login_required
def staff_update(request, staff_id):
    staff = Staff.objects.get(id = staff_id)
    if request.method == 'POST': 
        staff.name = request.POST['name']
        staff.phone = request.POST['phone']
        staff.email = request.POST['email']
        staff.save()
        messages.info(request, 'Staff Updated!')
        return redirect('userAdmin:staffs')
    return render(request, "userAdmin/staffs/staff_update_page.html", {"staff" : staff})

@login_required
def staff_delete(request, staff_id):
    if request.method == 'POST' :
        staff = Staff.objects.get(id=staff_id)
        staff.delete()
        messages.error(request,'Staff Deleted!')
        return redirect('userAdmin:staffs')
    return redirect('userAdmin:staffs')