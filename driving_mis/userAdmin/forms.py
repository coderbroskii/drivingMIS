from  django import forms
from .models import Student, Payment, Staff

class StudentRegisterForm(forms.ModelForm) :
    class Meta :
        model = Student
        exclude = ["slug"]
        fields = '__all__'

class PaymentRegistrationForm(forms.ModelForm) :
    class Meta :
        model = Payment
        fields = '__all__'

class StaffRegistrationForm(forms.ModelForm) :
    class Meta :
        model = Staff
        exclude = ["slug"]
        fields = '__all__'