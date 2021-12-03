from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from . models import Task

# Create your views here.

class CustomLoginView(LoginView):
    
    template_name = 'main/login.html'
    fields = '__all__' #Shows all field in form
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks') #When User Logs In send them to task list page


class RegisterForm(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') #When Registration is successfull it will return back to task list page

    def form_valid(self, form):
        user = form.save() # Save form
        if user is not None: # if user is successfully created
            login(self.request, user) 
        return super(RegisterForm, self).form_valid(form)

    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterForm, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs): # To prevent Users from Seeing Other Users ToDo List
        context = super().get_context_data(**kwargs)
        # context['color'] = 'red'
        context['tasks'] = context['tasks'].filter(user=self.request.user) #Logged In User
        context['count'] = context['tasks'].filter(completed=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            context['search_input'] = search_input # To avoid manually refreshing the page and go to template
        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'tasks'
    # template_name = 'main/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # template_name = 'main/task_create.html'
    fields = ['title', 'description','completed']  #Shows fields in form
    success_url = reverse_lazy('tasks') #Sending back user to tasks 


    def form_valid(self, form): # Automatic Select the User to loggedin User
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form) 


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description','completed']
    success_url = reverse_lazy('tasks') #When Updated go back to task list page


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


