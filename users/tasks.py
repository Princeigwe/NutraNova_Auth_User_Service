from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

@shared_task
def set_profile_image(image_url, user_email):
  try:
    user = User.objects.get(email=user_email)
    user.image = image_url
    user.save()
    return user
  except User.DoesNotExist:
    return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)