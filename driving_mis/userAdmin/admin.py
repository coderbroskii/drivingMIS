from django.contrib import admin
from .models import Student
from .models import Payment
from .models import Staff

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Staff)

