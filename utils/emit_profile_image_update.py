from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from utils.rabbitmq.publishers.user_data_update import send_user_data_update
import os


## todo: work on this feature for rabbitmq
User = get_user_model()
rabbitmq_message_type = os.environ.get('CHEF_DATA_UPDATE_MESSAGE_TYPE')


def emit_profile_image(image_url, user_email):
  try:
    user = User.objects.get(email=user_email)
    user.image = image_url
    user.save()
    print("user image updated")
    event_message = {
      "type": rabbitmq_message_type, # adding 'type' key to the message fixes the issue a consumer throws when is consumes different messages to work with
      "username": user.username,
      "image": user.image,
    }
    send_user_data_update(event_message)
  except User.DoesNotExist:
    return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)