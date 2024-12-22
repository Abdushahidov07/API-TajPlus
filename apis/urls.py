from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'apis'

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    path('profiles/', views.ProfileListView.as_view(), name='profile-list'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
    
    path('skills/', views.SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', views.SkillDetailView.as_view(), name='skill-detail'),
    
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    path('services/', views.ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:pk>/status/', views.ServiceStatusUpdateView.as_view(), name='service-status-update'),
    
    path('requests/', views.ServiceRequestListCreateView.as_view(), name='request-list-create'),
    path('requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='request-detail'),
    
    path('applications/', views.ApplicationServiceListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.ApplicationServiceDetailView.as_view(), name='application-detail'),
    
    path('chats/', views.ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    
    path('chats/<int:chat_id>/messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
]
