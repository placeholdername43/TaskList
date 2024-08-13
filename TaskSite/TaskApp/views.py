from datetime import datetime, timedelta

from django.shortcuts import render
from .models import Task


# Create your views here.

def landing_page(request):
    return render(request, 'landing_page.html')

def dashboard(request):
    next_30_days = datetime.now() + timedelta(days=30)
    tasks = Task.objects()
    tasks_due_in_30d = Task.objects.filter(due_by__lte = next_30_days)

    return render(request, 'dashboard.html')

def add_task(request):
    return render(request, 'add_task.html')

def login(request):
    return render(request, 'login.html')