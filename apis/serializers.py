from rest_framework import serializers
from .models import User, Profile, ServiceRequest, ApplicationService, Chat, Message, Skill, Category, Service

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'role', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'role', 'is_active')
        read_only_fields = ('is_active',)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'

class ServiceRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ('is_active', 'is_deleted', 'created_at', 'deleted_at')

class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ('title', 'description', 'image', 'location', 'price_min', 
                 'price_max', 'category', 'skills')

class ApplicationServiceSerializer(serializers.ModelSerializer):
    request = ServiceRequestSerializer(read_only=True)
    request_id = serializers.PrimaryKeyRelatedField(
        source='request',
        queryset=ServiceRequest.objects.all(),
        write_only=True
    )
    master = ProfileSerializer(read_only=True)
    
    class Meta:
        model = ApplicationService
        fields = ('id', 'request', 'request_id', 'master', 'descriptions', 'created_at', 'status')
        read_only_fields = ('created_at', 'master')

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('created_at',)

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    customer = UserSerializer(read_only=True)
    master = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ('is_active', 'is_deleted', 'created_at', 'deleted_at')

class ServiceSerializer(serializers.ModelSerializer):
    master = ProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('status', 'is_active', 'created_at', 'updated_at')

class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('title', 'description', 'price', 'category', 'skills', 'image')