from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.shortcuts import redirect, render
from .models import Task
from .forms import TaskForm
from lockdown.decorators import lockdown
from django.contrib.auth import logout



def landing_page(request):
    return render(request, 'landing_page.html')

@lockdown()
def dashboard(request):
    tasks = Task.objects.all()
    next_30_days = datetime.now() + timedelta(days=30)
    tasks_due_in_30d = Task.objects.filter(due_by__lte = next_30_days)
    urgent_tasks = tasks_due_in_30d.filter(is_urgent = True).count()

    line_chart_html = None
    pie_chart_html = None

    if tasks.exists():
        df = pd.DataFrame(list(tasks_due_in_30d.values('due_by', 'priority')))
        df['priority'] = df['priority'].apply(lambda x: dict(Task.PRIORITY_CHOICES).get(x))
        df['due_by'] = pd.to_datetime(df['due_by']).dt.date
        tasks_per_day = df.groupby('due_by').size().reset_index(name='count')
        line_chart_fig = px.line(tasks_per_day, x = "due_by", y = "count", markers = True)
        line_chart_html = pio.to_html(line_chart_fig, full_html=False)

        tasks_by_priority = df['priority'].value_counts().reset_index(name='count')
        tasks_by_priority.columns = ['priority','count']
        pie_chart_fig = px.pie(tasks_by_priority, names = 'priority', values = 'count', title='Tasks by Priority Due in the Next 30 Days')
        pie_chart_html = pio.to_html(pie_chart_fig, full_html=False)
    else:

        line_chart_fig = px.line(title = "No tasks due in the next 30 days")
        line_chart_html = pio.to_html(line_chart_fig, full_html = False)

        pie_chart_fig = px.pie(names=['No data'], values=[1], title = "no tasks by priotiy")
        pie_chart_html = pio.to_html(pie_chart_fig, full_html=False)


    taskData = {
        'tasks' : tasks,
        'tasks_due_in_30d' : tasks_due_in_30d,
        'total_urgent_tasks' : urgent_tasks,
        'line_chart':  line_chart_html,
        'pie_chart' : pie_chart_html,

    }

    logout_user(request)
    return render(request, 'dashboard.html', taskData)

def logout_user(request):
    logout(request)
    request.session.flush()

@lockdown()
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            logout_user(request)
            return redirect('landing_page')
    else:
        form= TaskForm()
    return render(request, 'add_task.html', {'form': form})

def login(request):
    return render(request, 'login.html')