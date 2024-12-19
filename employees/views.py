# filepath: /e:/Assignment FSD/employee_management_system/employees/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Employee
from .forms import EmployeeForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_panel')
    else:
        form = UserCreationForm()
    return render(request, 'employees/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('employee_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'employees/login.html', {'form': form})

@login_required
def admin_panel(request):
    return render(request, 'employees/admin_panel.html')

@login_required
def employee_dashboard(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'id')
    filter_by = request.GET.get('filter_by', '')

    employees = Employee.objects.all()

    if query:
        if filter_by == 'id':
            employees = employees.filter(id__icontains=query)
        elif filter_by == 'name':
            employees = employees.filter(name__icontains=query)
        elif filter_by == 'email':
            employees = employees.filter(email__icontains=query)
        elif filter_by == 'date_added':
            employees = employees.filter(createdate__icontains=query)
        else:
            employees = employees.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(mobile__icontains=query)
            )

    employees = employees.order_by(sort_by)

    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('employees/employee_list_partial.html', {'page_obj': page_obj, 'query': query, 'sort_by': sort_by, 'filter_by': filter_by})
        return JsonResponse({'html': html})

    return render(request, 'employees/employee_list.html', {'page_obj': page_obj, 'query': query, 'sort_by': sort_by, 'filter_by': filter_by})

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'employees/add_employee.html', {'form': form})

@login_required
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/edit_employee.html', {'form': form})

@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_dashboard')
    return render(request, 'employees/delete_employee.html', {'employee': employee})