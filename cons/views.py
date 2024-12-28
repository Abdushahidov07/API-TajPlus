from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django.urls import reverse_lazy
from .models import *

class UserList(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDetail(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

class UserCreate(CreateView):
    model = User
    template_name = 'user_form.html'
    fields = ['username', 'email', 'phone', 'role', 'is_active']
    success_url = reverse_lazy('user_list')

class UserUpdate(UpdateView):
    model = User
    template_name = 'user_form.html'
    fields = ['username', 'email', 'phone', 'role', 'is_active']
    success_url = reverse_lazy('user_list')

class UserDelete(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')




class SkillList(ListView):
    model = Skill
    template_name = 'skill_list.html'
    context_object_name = 'skills'

class SkillDetail(DetailView):
    model = Skill
    template_name = 'skill_detail.html'
    context_object_name = 'skill'

class SkillCreate(CreateView):
    model = Skill
    template_name = 'skill_form.html'
    fields = ['name', 'image']
    success_url = reverse_lazy('skill_list')

class SkillUpdate(UpdateView):
    model = Skill
    template_name = 'skill_form.html'
    fields = ['name', 'image']
    success_url = reverse_lazy('skill_list')

class SkillDelete(DeleteView):
    model = Skill
    template_name = 'skill_confirm_delete.html'
    success_url = reverse_lazy('skill_list')






class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

class CategoryCreate(CreateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')






class ProfileList(ListView):
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'profiles'

class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

class ProfileCreate(CreateView):
    model = Profile
    template_name = 'profile_form.html'
    fields = ['user', 'skills', 'image', 'address', 'remote', 'biography', 'date_of_birth']
    success_url = reverse_lazy('profile_list')

class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'profile_form.html'
    fields = ['skills', 'image', 'address', 'remote', 'biography', 'date_of_birth']
    success_url = reverse_lazy('profile_list')

class ProfileDelete(DeleteView):
    model = Profile
    template_name = 'profile_confirm_delete.html'
    success_url = reverse_lazy('profile_list')



class ServiceRequestList(ListView):
    model = ServiceRequest
    template_name = 'service_request_list.html'
    context_object_name = 'service_requests'

class ServiceRequestDetail(DetailView):
    model = ServiceRequest
    template_name = 'service_request_detail.html'
    context_object_name = 'service_request'

class ServiceRequestCreate(CreateView):
    model = ServiceRequest
    template_name = 'service_request_form.html'
    fields = ['title', 'description', 'image', 'user', 'location', 'price_min', 'price_max', 'status', 'category', 'skills', 'is_active']
    success_url = reverse_lazy('service_request_list')

class ServiceRequestUpdate(UpdateView):
    model = ServiceRequest
    template_name = 'service_request_form.html'
    fields = ['title', 'description', 'image', 'location', 'price_min', 'price_max', 'status', 'category', 'skills', 'is_active']
    success_url = reverse_lazy('service_request_list')

class ServiceRequestDelete(DeleteView):
    model = ServiceRequest
    template_name = 'service_request_confirm_delete.html'
    success_url = reverse_lazy('service_request_list')





class ServiceList(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceDetail(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

class ServiceCreate(CreateView):
    model = Service
    template_name = 'service_form.html'
    fields = ['title', 'description', 'price', 'master', 'category', 'skills', 'image', 'status', 'is_active']
    success_url = reverse_lazy('service_list')

class ServiceUpdate(UpdateView):
    model = Service
    template_name = 'service_form.html'
    fields = ['title', 'description', 'price', 'category', 'skills', 'image', 'status', 'is_active']
    success_url = reverse_lazy('service_list')

class ServiceDelete(DeleteView):
    model = Service
    template_name = 'service_confirm_delete.html'
    success_url = reverse_lazy('service_list')





class ApplicationServiceList(ListView):
    model = ApplicationService
    template_name = 'application_service_list.html'
    context_object_name = 'applications'

class ApplicationServiceDetail(DetailView):
    model = ApplicationService
    template_name = 'application_service_detail.html'
    context_object_name = 'application'

class ApplicationServiceCreate(CreateView):
    model = ApplicationService
    template_name = 'application_service_form.html'
    fields = ['request', 'master', 'descriptions', 'status', 'is_active']
    success_url = reverse_lazy('application_service_list')

class ApplicationServiceUpdate(UpdateView):
    model = ApplicationService
    template_name = 'application_service_form.html'
    fields = ['descriptions', 'status', 'is_active']
    success_url = reverse_lazy('application_service_list')

class ApplicationServiceDelete(DeleteView):
    model = ApplicationService
    template_name = 'application_service_confirm_delete.html'
    success_url = reverse_lazy('application_service_list')




class ChatList(ListView):
    model = Chat
    template_name = 'chat_list.html'
    context_object_name = 'chats'

class ChatDetail(DetailView):
    model = Chat
    template_name = 'chat_detail.html'
    context_object_name = 'chat'

class ChatCreate(CreateView):
    model = Chat
    template_name = 'chat_form.html'
    fields = ['request', 'customer', 'master', 'is_active']
    success_url = reverse_lazy('chat_list')

class ChatUpdate(UpdateView):
    model = Chat
    template_name = 'chat_form.html'
    fields = ['is_active']
    success_url = reverse_lazy('chat_list')

class ChatDelete(DeleteView):
    model = Chat
    template_name = 'chat_confirm_delete.html'
    success_url = reverse_lazy('chat_list')








class MessageList(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'

class MessageDetail(DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'

class MessageCreate(CreateView):
    model = Message
    template_name = 'message_form.html'
    fields = ['chat', 'sender', 'message_text', 'image']
    success_url = reverse_lazy('message_list')  
class MessageUpdate(UpdateView):
    model = Message
    template_name = 'message_form.html'
    fields = ['message_text', 'image']
    success_url = reverse_lazy('message_list')  

class MessageDelete(DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('message_list') 


from django.shortcuts import render

# Home page view
def home(request):
    return render(request, 'home.html')