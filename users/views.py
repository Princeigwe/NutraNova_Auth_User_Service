from django.shortcuts import render
from django.contrib.auth import get_user_model
import random
import string
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

{
  "sub": "google-oauth2|102871429371675148459",
  "given_name": "Prince",
  "family_name": "Igwe",
  "nickname": "igwep297",
  "name": "Prince Igwe",
  "picture": "https://lh3.googleusercontent.com/a/ACg8ocI8qloD1xOLTj0OsAMpX4tUOxF2VHMu5i_F3rYCVEB-wCo=s96-c",
  "locale": "en",
  "updated_at": "2023-09-29T01:30:30.292Z",
  "email": "igwep297@gmail.com",
  # "email_verified": true
}

User = get_user_model()

def create_random_password_string(length):
  letters = string.ascii_letters
  result_string = ''.join(random.choice(letters) for i in range(length))
  return result_string


def create_user(request, username, email, first_name, last_name, password=None):
  try:
    user = User.objects.get( Q(username=username) | Q(email=email))
    return JsonResponse({"error": "User with email or username already exists"})

  except User.DoesNotExist:
    user.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)

    if password is not None:
      user.set_password(password)
    else:
      password = create_random_password_string(12)
      user.set_password(password)
    
    user.save()
    return JsonResponse({ "message": "User created successfully.", "data": user }, status=200)