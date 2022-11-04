from django.shortcuts import render,redirect
from django.shortcuts import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from .forms import PositionForm
from django.db import transaction

class userlogin(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_redirect_url(self):
        return reverse_lazy('tasks')

class Register(FormView):
    template_name='registration/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('home')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user) 
        return super(Register,self).form_valid(form)

    def get(self,request,*args, **kwargs):
        if self.request.user.is_authenticated:
             return HttpResponseRedirect('home')
        return super(Register,self).get(request,*args, **kwargs)    
                


class taskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='tasks'

    def get_context_data(self, *args,**kwargs):
        context=super(taskList,self).get_context_data(*args,**kwargs)
        context['tasks']=self.model.objects.all()
        context['count']=self.model.objects.filter(complete=False).count()
        
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']= context['tasks'].filter(title__startswith= search_input)
        context['tasks']=search_input
               
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
    fields=['title','description','complete']
    success_url=reverse_lazy('home')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(taskCreate,self).form_valid(form)   

class taskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('home')

class taskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('home') 

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))             