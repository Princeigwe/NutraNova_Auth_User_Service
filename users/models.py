import django
django.setup()

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from enums import choices
from multiselectfield import MultiSelectField

from .managers import CustomUserManager

User = settings.AUTH_USER_MODEL

# Create your models here.


class CustomUser(AbstractUser):
  image         = models.URLField(max_length=500, default="https://www.gravatar.com/avatar")
  username      = models.CharField(max_length=20, unique=True)
  email         = models.EmailField(_("email address"), unique=True)
  first_name    = models.CharField(max_length=20)
  last_name     = models.CharField(max_length=20)
  password      = models.CharField()
  # is_staff      = models.BooleanField(default=False)
  # is_active     = models.BooleanField(default=True)

  age                 = models.CharField(max_length=3, default=12)
  gender              = models.CharField(max_length=6, choices=choices.GENDER_CHOICES, default="MALE")
  role                = models.CharField(max_length=30, choices=choices.ROLE_CHOICES, default="USER")
  dietary_preference  = models.CharField(max_length=50, choices=choices.DIETARY_PREFERENCES_CHOICES, blank=True)
  health_goal         = models.CharField(max_length=50, choices=choices.HEALTH_GOALS_CHOICES, default="OVERALL_WELLNESS")
  allergens           = MultiSelectField(choices=choices.ALLERGEN_CHOICES, blank=True, max_length=50)
  activity_level      = models.CharField(max_length=50, choices=choices.ACTIVITY_LEVELS)
  cuisines            = MultiSelectField(choices=choices.CUISINES_CHOICES, max_length=50, default="ITALIAN")
  medical_conditions  = MultiSelectField(choices=choices.MEDICAL_CONDITIONS_CHOICES, blank=True, max_length=50)
  taste_preferences   = MultiSelectField(choices=choices.TASTE_PREFERENCES_CHOICES, blank=True, max_length=50)


  # field for dietician/health practitioners
  specialization          = models.CharField(max_length=50, choices=choices.HEALTH_PRACTITIONER_SPECIALIZATION_CHOICES, blank=True, null=True)

  professional_statement  = models.TextField(max_length=200, blank=True, null=True)
  availability            = models.BooleanField(blank=True, null=True)
  is_on_boarded           = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
    return self.email



class UserFollowing(models.Model):
  user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
  following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    f"{self.user_id} follows {self.following_user_id}"