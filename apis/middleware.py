from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.open_urls:
            return redirect(self.login_url)
        
        # Check for admin status on protected URLs
        if (request.user.is_authenticated and 
            not request.user.is_staff and 
            request.path_info not in self.open_urls):
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect(self.login_url)
            
        return self.get_response(request)
