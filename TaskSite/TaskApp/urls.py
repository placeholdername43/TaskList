from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_task', views.add_task, name='add_task'),
    path('login', views.login, name='login'),
]