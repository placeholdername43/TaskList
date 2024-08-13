from django.shortcuts import render
from .models import Task

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def dashboard(request):
    tasks = Task.objects()

    return render(request, 'pages/dashboard.html')