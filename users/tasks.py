from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
# from utils.kafka.produce.user_data_update import send_user_data_update

## todo: work on this feature for rabbitmq
# User = get_user_model()

@shared_task
def set_profile_image(image_url, user_email):
  # try:
  #   user = User.objects.get(email=user_email)
  #   user.image = image_url
  #   user.save()
  #   # return user
  #   print("user image updated")
  #   kafka_message = {
  #     "username": user.username,
  #     "image": user.image,
  #   }
  #   send_user_data_update(kafka_message)
  #   print("kafka message sent...")
  # except User.DoesNotExist:
  #   return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
  pass