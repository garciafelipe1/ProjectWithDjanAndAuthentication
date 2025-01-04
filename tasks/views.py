from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from http.client import HTTPResponse
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request,user)
                return redirect('tasks')
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "username already exists"},
                )
    return render(
        request,
        "signup.html",
        {"form": UserCreationForm, "error": "PASSWORD Do not match"},
    )

def tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = None  # O una lista vacía []

    return render(request, 'tasks.html', {'tasks': tasks, 'user_authenticated': request.user.is_authenticated})

def create_task(request):


    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else: 
        try:
            form= TaskForm(request.POST)
            new_task=form.save(commit=False)
            new_task.user =request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'please provide valid dates'
            })

def task_detail(request,task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else: 
        try:
            task=get_object_or_404(Task, pk=task_id, user=request.user)
            form=TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{
                'task': task,
                'form': form,
                'error': 'error updating '
            })



def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render (request, 'signin.html',{
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None: 
            return render (request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
    
    
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    task.complete = True
    task.save()
    return redirect('tasks')


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
      task.delete()
      return redirect('tasks')