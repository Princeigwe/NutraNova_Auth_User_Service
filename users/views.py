from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core import serializers
import random
import string
from django.db.models import Q
from django.http import HttpResponse
import json
from utils.jwt_encode_decode import encode_access_token, decode_access_token
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from file.views import upload_image_to_cloudinary
from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
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


@api_view(['POST'])
@parser_classes([MultiPartParser])
def set_profile_image(request):
    authorization_header = request.headers.get("Authorization") 
    if not authorization_header:
        return Response({"message": "Unauthorized request"}, status=status.HTTP_400_BAD_REQUEST)
    parts = authorization_header.split(" ")
    token = parts[1] 
    decoded_data = decode_access_token(token) 
    user_email = decoded_data['email']

    upload_image = upload_image_to_cloudinary(request)
    profile_image = upload_image["secure_url"]
    print(profile_image)
    user = User.objects.get(email=user_email)
    user.image = profile_image
    user.save()
    serialized_user = serializers.serialize('json', [user, ])
    response = {
        "user": serialized_user
    }
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type='application/json')
