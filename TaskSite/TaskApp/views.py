from datetime import datetime, timedelta

from django.shortcuts import redirect, render
from .models import Task
from .forms import TaskForm

# Create your views here.

def landing_page(request):
    return render(request, 'landing_page.html')

def dashboard(request):
    tasks = Task.objects.all()
    next_30_days = datetime.now() + timedelta(days=30)
    tasks_due_in_30d = Task.objects.filter(due_by__lte = next_30_days)
    urgent_tasks = tasks_due_in_30d.filter(is_urgent = True).count()

    taskData = {
        'tasks' : tasks,
        'tasks_due_in_30d' : tasks_due_in_30d,
        'total_urgent_tasks' : urgent_tasks,

    }

    return render(request, 'dashboard.html', taskData)

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing_page')
    else:
        form= TaskForm()
    return render(request, 'add_task.html', {'form': form})

def login(request):
    return render(request, 'login.html')