from django.shortcuts import render, redirect
from django.contrib.auth import *

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('dashboard:login')

def login_view(request, username, password):
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
    
