from django.db import models
from django.utils.text import slugify
import uuid

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    course = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Bike'),
            ('B', 'Car'),
            ('K', 'Scooter')
        ]
    )
    enrollment_date = models.DateField()
    total_fee = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    fees_paid = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    @property
    def balance(self):
        return self.total_fee - self.fees_paid

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:  # only create slug if it's empty
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:4]
        super().save(*args, **kwargs)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    amountPaid = models.IntegerField()
    paymentDate = models.DateField()
    paymentMethod = models.CharField(max_length=15, 
    choices=
    [
        ('Cash', 'Cash'),
        ('Online', 'Online Payment'),
    ], default='Cash'
        )
    
    def __str__(self):
        return self.student.name
    
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