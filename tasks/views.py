from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from http.client import HTTPResponse

# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username= request.POST['username'], password= request.POST['password1'])
                user.save()
                return HttpResponse('user created succesfuly')
            except:
                return HttpResponse('user already exist')
        return HttpResponse('password do not match')
    