from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def helloword(request):
    return HttpResponse ('Hello word')
    