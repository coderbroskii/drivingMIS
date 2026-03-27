from django.db import models
from django.utils.text import slugify
from datetime import timedelta
from django.core.exceptions import ValidationError
import uuid

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    course = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Bike(15 Days)'),
            ('B', 'Car(30 Days)'),
            ('K', 'Scooter(15 Days)')
        ]
    )
    enrollment_date = models.DateField()
    total_fee = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    fees_paid = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    @property
    def end_date(self):
        if self.course == 'A':   
                days = 15
        elif self.course == 'K': 
                days = 15
        elif self.course == 'B': 
                days = 30
        else:
                days = 0

        return self.enrollment_date + timedelta(days=days)

    @property
    def balance(self):
        return self.total_fee - self.fees_paid

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:4]
        super().save(*args, **kwargs)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amountPaid = models.IntegerField()
    paymentDate = models.DateField()
    paymentMethod = models.CharField(
        max_length=15,
        choices=[
            ('Cash', 'Cash'),
            ('Online', 'Online Payment'),
        ],
        default='Cash'
    )

    def save(self, *args, **kwargs):
        current_amount = int(self.amountPaid)
        if self.pk:
            old_payment = Payment.objects.get(pk=self.pk)
            old_amount = int(old_payment.amountPaid)
            diff = current_amount - old_amount
        else:
            diff = current_amount
        if self.student.fees_paid + diff > self.student.total_fee:
            raise ValidationError("Payment exceeds total fee")
        self.student.fees_paid += diff
        self.student.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.student.name
    
    def delete(self):
        self.student.fees_paid -= self.amountPaid
        self.student.save()
        super().delete()

class Staff(models.Model) : 
    name = models.CharField(max_length=15)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:4]
        super().save(*args,**kwargs)