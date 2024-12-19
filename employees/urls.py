# filepath: /e:/Assignment FSD/employee_management_system/employees/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
]