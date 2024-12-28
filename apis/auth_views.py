from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

def is_admin(user):
    return user.is_staff

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('home')
        else:
            messages.error(request, 'Access denied. Admin privileges required.')
            logout(request)
            return redirect('login')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0)
                
                return redirect('home')
            else:
                messages.error(request, 'Access denied. Admin privileges required.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin, login_url='login')
def home_view(request):
    return render(request, 'home.html')
