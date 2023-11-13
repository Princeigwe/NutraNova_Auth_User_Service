from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core import serializers
import random
import string
from django.db.models import Q
from django.http import HttpResponse
import json
from utils.jwt_encode_decode import encode_access_token
from django.core import serializers

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
        payload = {
            "username": user_data["username"],
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
        }
        access_token = encode_access_token(payload)
        user_data["access_token"] = access_token
        return HttpResponse(json.dumps(user_data), content_type="application/json")

    except User.DoesNotExist:
        password = create_random_password_string(5)
        print(password)
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        print(user)
        user.save()

        serialized_data = serializers.serialize("json", [user])
        user_data = json.loads(serialized_data)[0]['fields']  # Parse JSON and access 'fields'
        print(user_data)
        payload = {
            "username": user_data["username"],
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
        }
        access_token = encode_access_token(payload)
        user_data["access_token"] = access_token
        return HttpResponse(json.dumps(user_data), content_type="application/json")
