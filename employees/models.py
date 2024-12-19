# filepath: employees/models.py
from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name