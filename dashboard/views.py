from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from authentication.views import login_view

# Create your views here.
def dashboard_login(request):
    if request.method == "POST": #To be improved with a Django form to return error messages when wrong infrmation is submited and for better validations
        username = request.POST['login-email']
        password = request.POST['password']
        login_view(request, username, password)
        if request.user is not None and not request.user == "AnonymousUser":
            return redirect('dashboard:main')


        
    return render(request, 'frontend/page_ready_login.html')

@login_required(login_url='dashboard:login')
def dashboard_main(request):
    return redirect('services:services_overview')
    #return render(request, 'services_overview.html')

