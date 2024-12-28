from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse

def is_admin(user):
    return user.is_staff

def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('apis:admin_dashboard')
        else:
            messages.error(request, 'You do not have admin privileges.')
            logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('apis:admin_dashboard')
            else:
                messages.error(request, 'You do not have admin privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('apis:admin_login')

@login_required(login_url='apis:admin_login')
@user_passes_test(is_admin, login_url='apis:admin_login')
def admin_dashboard(request):
    context = {
        'section': 'dashboard',
        'title': 'Dashboard'
    }
    return render(request, 'base.html', context)
