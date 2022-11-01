from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from .models import Task


class taskList(ListView):
    model=Task
    context_object_name='tasks'
