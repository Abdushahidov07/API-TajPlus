from django.urls import path
from .views import *

urlpatterns = [
    path('users/',UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/',UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    path('skills/',SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/',SkillRetrieveUpdateDestroyView.as_view(), name='skill-detail'),

    path('categories/',CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/',CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('profiles/',ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/',ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),

    path('service-requests/',ServiceRequestListCreateView.as_view(), name='service-request-list-create'),
    path('service-requests/<int:pk>/',ServiceRequestRetrieveUpdateDestroyView.as_view(), name='service-request-detail'),

    path('applications/',ApplicationServiceListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/',ApplicationServiceRetrieveUpdateDestroyView.as_view(), name='application-detail'),

    path('chats/',ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/',ChatRetrieveUpdateDestroyView.as_view(), name='chat-detail'),

    path('messages/',MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/',MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
]
