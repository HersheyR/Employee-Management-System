# filepath: /e:/Assignment FSD/employee_management_system/employees/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee
from django.core.exceptions import ValidationError
import re

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class EmployeeForm(forms.ModelForm):
    DESIGNATION_CHOICES = [
        ('HR', 'HR'),
        ('Sales', 'Sales'),
        ('Manager', 'Manager'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    COURSE_CHOICES = [
        ('MCA', 'MCA'),
        ('BCA', 'BCA'),
        ('BSC', 'BSC'),
    ]

    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    course = forms.MultipleChoiceField(choices=COURSE_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Employee
        fields = ['image', 'name', 'email', 'mobile', 'designation', 'gender', 'course', 'is_active']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            if Employee.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Email already exists")
        else:
            if Employee.objects.filter(email=email).exists():
                raise ValidationError("Email already exists")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d+$', mobile):
            raise ValidationError("Mobile number must be numeric")
        return mobile

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.endswith(('.jpg', '.png')):
                raise ValidationError("Only .jpg and .png files are allowed")
        elif not self.instance.pk:
            raise ValidationError("This field is required.")
        return image