from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(_("email address"), unique=True)
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  password = models.CharField(max_length=50)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

  objects = CustomUserManager()

  def __str__(self):
    return f'{self.email}'

# class User(models.Model):
#   first_name = models.CharField(max_length=20)
#   last_name = models.CharField(max_length=20)
#   email = models.CharField(max_length=20)
#   username = models.CharField(max_length=20)
#   password = models.CharField(max_length=50)
  
#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = []

# def __str__(self):
#   return f'{self.first_name} {self.last_name}'