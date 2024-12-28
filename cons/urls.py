from django.urls import path
from . import views
from .views import *


urlpatterns = [
    #home
    path('', views.home, name='home'),
    # User URLs
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/create/', views.UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    # Skill URLs
    path('skills/', views.SkillList.as_view(), name='skill_list'),
    path('skills/create/', views.SkillCreate.as_view(), name='skill_create'),
    path('skills/<int:pk>/', views.SkillDetail.as_view(), name='skill_detail'),
    path('skills/<int:pk>/update/', views.SkillUpdate.as_view(), name='skill_update'),
    path('skills/<int:pk>/delete/', views.SkillDelete.as_view(), name='skill_delete'),

    # Category URLs
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),

    # Profile URLs
    path('profiles/', views.ProfileList.as_view(), name='profile_list'),
    path('profiles/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profiles/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('profiles/<int:pk>/delete/', views.ProfileDelete.as_view(), name='profile_delete'),

    # ServiceRequest URLs
    path('service-requests/', views.ServiceRequestList.as_view(), name='service_request_list'),
    path('service-requests/create/', views.ServiceRequestCreate.as_view(), name='service_request_create'),
    path('service-requests/<int:pk>/', views.ServiceRequestDetail.as_view(), name='service_request_detail'),
    path('service-requests/<int:pk>/update/', views.ServiceRequestUpdate.as_view(), name='service_request_update'),
    path('service-requests/<int:pk>/delete/', views.ServiceRequestDelete.as_view(), name='service_request_delete'),

    # Service URLs
    path('services/', views.ServiceList.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreate.as_view(), name='service_create'),
    path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),
    path('services/<int:pk>/update/', views.ServiceUpdate.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDelete.as_view(), name='service_delete'),

    # ApplicationService URLs
    path('applications/', views.ApplicationServiceList.as_view(), name='application_service_list'),
    path('applications/create/', views.ApplicationServiceCreate.as_view(), name='application_service_create'),
    path('applications/<int:pk>/', views.ApplicationServiceDetail.as_view(), name='application_service_detail'),
    path('applications/<int:pk>/update/', views.ApplicationServiceUpdate.as_view(), name='application_service_update'),
    path('applications/<int:pk>/delete/', views.ApplicationServiceDelete.as_view(), name='application_service_delete'),

    # Chat URLs
    path('chats/', views.ChatList.as_view(), name='chat_list'),
    path('chats/create/', views.ChatCreate.as_view(), name='chat_create'),
    path('chats/<int:pk>/', views.ChatDetail.as_view(), name='chat_detail'),
    path('chats/<int:pk>/update/', views.ChatUpdate.as_view(), name='chat_update'),
    path('chats/<int:pk>/delete/', views.ChatDelete.as_view(), name='chat_delete'),

    # Message URLs
    path('messages/', views.MessageList.as_view(), name='message_list'),
    path('messages/create/', views.MessageCreate.as_view(), name='message_create'),
    path('messages/<int:pk>/', views.MessageDetail.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', views.MessageUpdate.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.MessageDelete.as_view(), name='message_delete'),
]
