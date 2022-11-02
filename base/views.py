from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

class login(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_redirect_url(self):
        return reverse_lazy('tasks')


class taskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='tasks'

    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['tasks']=Task.objects.all()
        context['count']=context['tasks'].filter(complete=False).count()
        return context
    def get_queryset(self):
        query_set= super().get_queryset()
        return  query_set.filter(user=self.request.user) 

class taskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    template_name='base/task_detail.html'

class taskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields='__all__'
    success_url=reverse_lazy('home')   

class taskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields='__all__'
    success_url=reverse_lazy('home')

class taskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('home')          