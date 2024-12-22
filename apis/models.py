from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    class UserRole(models.TextChoices):
        CLIENT = 'CL', 'Клиент'
        MASTER = 'MS', 'Мастер'

    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=2, 
        choices=UserRole.choices, 
        default=UserRole.CLIENT
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Add related_name to fix the clash with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def str(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_master(self):
        return self.role == self.UserRole.MASTER

    @property
    def is_client(self):
        return self.role == self.UserRole.CLIENT

class Skill(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/skills/', null=True, blank=True)

    def str(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, blank=True)
    image = models.ImageField(upload_to='media/users/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    remote = models.BooleanField(default=False)
    biography = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def str(self):
        return f"{self.user.username}'s Profile"

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Черновик'
        OPEN = 'OP', 'Открыт'
        IN_PROGRESS = 'IP', 'В работе'
        COMPLETED = 'CM', 'Выполнен'
        CANCELLED = 'CN', 'Отменен'

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/service_requests/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    location = models.TextField()
    price_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.DRAFT
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.title} ({self.get_status_display()})"

class Service(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Черновик'
        ACTIVE = 'AC', 'Активный'
        PAUSED = 'PA', 'Приостановлен'
        COMPLETED = 'CM', 'Завершен'
        CANCELLED = 'CN', 'Отменен'
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    master = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    image = models.ImageField(upload_to='media/services/', null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f"{self.title} ({self.get_status_display()})"

class ApplicationService(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PD', 'В ожидании'
        ACCEPTED = 'AC', 'Принята'
        REJECTED = 'RJ', 'Отклонена'
        COMPLETED = 'CM', 'Выполнена'

    request = models.ForeignKey(ServiceRequest,on_delete=models.CASCADE, related_name='applications')
    master = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='service_applications')
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.PENDING
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"Заявка от {self.master.user.username} на {self.request.title} ({self.get_status_display()})"

class Chat(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name='customer_chats', on_delete=models.CASCADE)
    master = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"Chat for {self.request.title}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    image = models.ImageField(upload_to='media/messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Message in {self.chat}"


