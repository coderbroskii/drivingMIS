from django.shortcuts import render, redirect
from .models import Student,Payment,Staff
from django.db.models import Sum  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

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

        if not name.strip():
            messages.error(request, "Name cannot be empty")
            return redirect('userAdmin:addStudent')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('userAdmin:addStudent')
        
        if Student.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect('userAdmin:addStudent')

        if not total_fee.isdigit() or int(total_fee) <= 0:
            messages.error(request, "Total fee must be a positive number")
            return redirect('userAdmin:addStudent')

        if not fees_paid.isdigit() or int(fees_paid) < 0:
            messages.error(request, "Fees paid cannot be negative")
            return redirect('userAdmin:addStudent')

        if int(fees_paid) > int(total_fee):
            messages.error(request, "Fees paid cannot exceed total fee")
            return redirect('userAdmin:addStudent')
        
        try:
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
        except IntegrityError:
            messages.error(request, "Phone number already exists")
            return redirect('userAdmin:addStudent')
    return render(request, "userAdmin/students/student_add_page.html")

@login_required
def student_update(request, id):
    student = get_object_or_404(Student, id=id)

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
            return redirect('userAdmin:updateStudent', id=id)

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('userAdmin:updateStudent', id=id)

        if not total_fee.isdigit() or int(total_fee) <= 0:
            messages.error(request, "Total fee must be positive")
            return redirect('userAdmin:updateStudent', id=id)

        if not fees_paid.isdigit() or int(fees_paid) < 0:
            messages.error(request, "Fees paid cannot be negative")
            return redirect('userAdmin:updateStudent', id=id)

        if int(fees_paid) > int(total_fee):
            messages.error(request, "Fees paid cannot exceed total fee")
            return redirect('userAdmin:updateStudent', id=id)
        
        student.name = name
        student.phone = phone
        student.address = address
        student.course = course
        student.enrollment_date = enrollment_date
        student.total_fee = total_fee
        student.fees_paid = fees_paid
        student.notes = notes
        student.save()

        messages.success(request, "Student Record Updated!")
        return redirect('userAdmin:students')
    return render(request,"userAdmin/students/student_update_page.html",{"student": student}
    )

@login_required
def student_delete(request, id):
    if request.method == 'POST' :
        student = Student.objects.get(id=id)
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
        # student_slug = request.POST['student']
        student_id = request.POST['student']  
        amount = int(request.POST['amountPaid'])   # converting to int
        date = request.POST['paymentDate']
        method = request.POST['paymentMethod']

        student_obj = Student.objects.get(id=student_id)
        if amount <= 0:
            messages.error(request, "Payment must be greater than zero")
        elif amount > student_obj.balance:
            messages.error(request, "Payment exceeds remaining balance")
        else:
            payment = Payment(
            student=student_obj,
            amountPaid=amount,
            paymentDate=date,
            paymentMethod=method,
        )
            payment.save()   #this saves the payment

            messages.success(request, "Payment Recorded!")
        return redirect('userAdmin:payments')

    return render(
        request,"userAdmin/payments/payment_add_page.html",{'students': students}
    )

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
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not name.strip():
            messages.error(request, "Name cannot be empty")
            return redirect('userAdmin:addStaff')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('userAdmin:addStaff')
        
        if Staff.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect('userAdmin:addStaff')
        
        if '@' not in email.strip() or '.' not in email.strip().split('@')[-1] or len(email.strip()) < 5:
            messages.error(request, "Enter a valid email address")
            return redirect('userAdmin:addStudent')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('userAdmin:addStaff')
        
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=name)
        user.save()

        # this saves to existing staff model
        Staff.objects.create(
            name=name,
            phone=phone,
            email=email,
        )
        messages.success(request,'Staff Added!')
        return redirect ('userAdmin:staffs')
    return render(request, "userAdmin/staffs/staff_add_page.html")

@login_required
def staff_update(request, staff_id):
    staff = Staff.objects.get(id = staff_id)
    
    if request.method == 'POST': 
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        if not name.strip():
            messages.error(request, "Name cannot be empty")
            return redirect('userAdmin:updateStaff', staff_id = staff_id)

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('userAdmin:updateStaff', staff_id=staff_id)
        
        if Staff.objects.filter(phone=phone).exclude(id=staff_id).exists():
            messages.error(request, "Phone number already exists")
            return redirect('userAdmin:updateStaff' , staff_id=staff_id)
        
        if '@' not in email.strip() or '.' not in email.strip().split('@')[-1] or len(email.strip()) < 5:
            messages.error(request, "Enter a valid email address")
            return redirect('userAdmin:updateStaff' , staff_id=staff_id)
        
        staff.name = name
        staff.phone = phone
        staff.email = email

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