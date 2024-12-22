from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .permissions import IsMasterOrReadOnly, IsServiceOwner, CanChangeServiceStatus

# Authentication Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

# User Views
class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'phone']

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Profile Views
class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['skills', 'remote']
    search_fields = ['user__username', 'biography']

    def get_queryset(self):
        return Profile.objects.filter(user__is_active=True, user__role='MS')

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

# Skill Views
class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

# Category Views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Service Request Views
class ServiceRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'status', 'skills']
    search_fields = ['title', 'description']

    def get_queryset(self):
        if self.request.user.is_master:
            return ServiceRequest.objects.filter(status='OP', is_active=True)
        return ServiceRequest.objects.filter(user=self.request.user, is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceRequestCreateSerializer
        return ServiceRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='OP')

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_master:
            return ServiceRequest.objects.filter(is_active=True)
        return ServiceRequest.objects.filter(user=self.request.user, is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Application Service Views
class ApplicationServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        if self.request.user.is_master:
            return ApplicationService.objects.filter(master__user=self.request.user)
        return ApplicationService.objects.filter(request__user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_master:
            return Response(
                {'error': 'Only masters can create applications'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            profile = Profile.objects.get(user=self.request.user)
            application = serializer.save(master=profile, status='PD')  # PD - Pending/В ожидании
            
            # Если это заявка от мастера к клиенту (отклик на запрос)
            if application.request:
                # Автоматически создаем чат при создании заявки
                Chat.objects.get_or_create(
                    request=application.request,
                    customer=application.request.user,
                    master=profile,
                    defaults={
                        'is_active': True
                    }
                )
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found. Please complete your profile first'},
                status=status.HTTP_400_BAD_REQUEST
            )

class ApplicationServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_master:
            return ApplicationService.objects.filter(master__user=self.request.user)
        return ApplicationService.objects.filter(request__user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        # Если статус меняется на "Принята", создаем чат
        if instance.status == 'AC':  # AC - Accepted/Принята
            Chat.objects.get_or_create(
                request=instance.request,
                customer=instance.request.user,
                master=instance.master,
                defaults={
                    'is_active': True
                }
            )

# Chat Views
class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_master:
            return Chat.objects.filter(master__user=self.request.user, is_active=True)
        return Chat.objects.filter(customer=self.request.user, is_active=True)

    def perform_create(self, serializer):
        if self.request.user.is_master:
            serializer.save(master=self.request.user.profile)
        else:
            serializer.save(customer=self.request.user)

class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_master:
            return Chat.objects.filter(master__user=self.request.user)
        return Chat.objects.filter(customer=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Message Views
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = Chat.objects.get(id=chat_id)
        serializer.save(chat=chat, sender=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

# Service Views
class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsMasterOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'status', 'skills']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        if self.request.user.is_master:
            return queryset | Service.objects.filter(
                master__user=self.request.user,
                status='DR'
            )
        return queryset.filter(status='AC')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateSerializer
        return ServiceSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_master:
            return Response(
                {'error': 'Only masters can create services'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            profile = Profile.objects.get(user=self.request.user)
            serializer.save(master=profile, status='DR')
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found. Please complete your profile first'},
                status=status.HTTP_400_BAD_REQUEST
            )

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceOwner, CanChangeServiceStatus]

    def get_queryset(self):
        if self.request.user.is_master:
            return Service.objects.filter(master__user=self.request.user)
        return Service.objects.filter(status='AC', is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ServiceStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceOwner, CanChangeServiceStatus]
    
    def get_queryset(self):
        return Service.objects.filter(master__user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        instance.status = new_status
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
