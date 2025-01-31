from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
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
            "image": user_data["image"],
            "username": user_data["username"],
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "dob": user_data["dob"],
            "gender": user_data["gender"],
            "role": user_data["role"],
            "dietary_preference": user_data["dietary_preference"],
            "taste_preferences": user_data["taste_preferences"],
            "health_goal": user_data["health_goal"],
            "allergens": user_data["allergens"],
            "activity_level": user_data["activity_level"],
            "cuisines": user_data["cuisines"],
            "medical_conditions": user_data["medical_conditions"],
            "is_on_boarded": user_data["is_on_boarded"],
            "vote_strength": user_data["vote_strength"],
            "is_verified": user_data["is_verified"]
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
            "gender": user_data["gender"],
            "role": user_data["role"],
            "dietary_preference": user_data["dietary_preference"],
            "taste_preferences": user_data["taste_preferences"],
            "health_goal": user_data["health_goal"],
            "allergens": user_data["allergens"],
            "activity_level": user_data["activity_level"],
            "cuisines": user_data["cuisines"],
            "medical_conditions": user_data["medical_conditions"],
            "is_on_boarded": user_data["is_on_boarded"],
        }
        access_token = encode_access_token(payload)
        user_data["access_token"] = access_token
        return HttpResponse(json.dumps(user_data), content_type="application/json")


#* superusers will authenticate directly on the API without an OpenID provider. This will be done with GraphQL
def create_superuser(email: str, username: str, password: str):
    try:
        superuser = User.objects.get(email=email)
        return superuser
    except User.DoesNotExist:
        superuser = User.objects.create_superuser(email=email, username=username)
        superuser.set_password(password)
        superuser.save()
        return superuser


def authenticate_superuser(username: str, password: str):
    superuser = authenticate(username=username, password=password)
    if superuser is not None:
        payload = {
            "email": superuser.email,
            "username": superuser.username,
            "is_superuser": superuser.is_superuser,
            "is_on_boarded": superuser.is_on_boarded,
        }
        access_token = encode_access_token(payload)
        return {
            "superuser": superuser,
            "jwt": access_token
        }
    else:
        return{
            "message": "Invalid credentials."
        }