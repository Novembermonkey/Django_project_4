from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50 ,unique=True)

    def __str__(self):
        return self.name



class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, default='')
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='users/profile_pics', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, related_name='users')
    photo = models.ImageField(upload_to='users/photos', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email