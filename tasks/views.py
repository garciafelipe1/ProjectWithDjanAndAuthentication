from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from http.client import HTTPResponse
from .forms import TaskForm
from .models import Task

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
    tasks = Task.objects.filter(user=request.user )  # Cambié 'task' a 'tasks' para ser consistente
    
    return render(request, 'tasks.html', {
        'tasks': tasks  # Pasamos 'tasks' correctamente al contexto
    })


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
    task=get_object_or_404(Task,pk=task_id)
    return render(request, 'task_detail.html',{
        'task': task
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
    