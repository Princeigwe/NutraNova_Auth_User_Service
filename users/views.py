from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core import serializers
import random
import string
from django.db.models import Q
from django.http import HttpResponse
import json

# Create your views here.

User = get_user_model()

def create_random_password_string(length):
  letters = string.ascii_letters
  result_string = ''.join(random.choice(letters) for i in range(length))
  return result_string


def oidc_get_or_create_user(request, username, email, first_name, last_name):
    try:
        user = User.objects.get(Q(username=username) | Q(email=email))
        serialized_data = serializers.serialize("json", [user])
        user_data = json.loads(serialized_data)[0]['fields']  # Parse JSON and access 'fields'

        return HttpResponse(json.dumps(user_data), content_type="application/json")

    except User.DoesNotExist:
        password = create_random_password_string(5)
        print(password)
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        serialized_data = serializers.serialize("json", [user])
        user_data = json.loads(serialized_data)[0]['fields']  # Parse JSON and access 'fields'

        return HttpResponse(json.dumps(user_data), content_type="application/json")

    # dict_user = model_to_dict(user)
    # serialized_user = json.dumps(dict_user)
    # return JsonResponse({ "message": "User created successfully.", "data": serialized_user }, status=200)