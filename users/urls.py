from django.urls import path
from .views import set_profile_image

app_name = 'users'

urlpatterns = [
  path('profile-image', set_profile_image)
]