from utils.jwt_encode_decode import decode_access_token
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def resolve_onboardUser(_, info, input:dict):
  # request = info.context["request"]
  # user = request.user
  request = info.context["request"]
  authorization_header = request.headers.get("Authorization")
  parts = authorization_header.split(" ")
  token = parts[1]
  decoded_data = decode_access_token(token)
  print(decoded_data)
  user_email = decoded_data['email']
  username = decoded_data['username']
  user_firstname = decoded_data['first_name']
  user_lastname = decoded_data['last_name']
  print(user_email)
  print(username)
  print(user_firstname)
  print(user_lastname)

  clean_input = {
    "age":                  input["age"],
    "gender":               input["gender"],
    "role":                 input["role"],
    "dietaryPreference":    input["dietaryPreference"],
    "healthGoal":           input["healthGoal"],
    "allergens":            input["allergens"],
    "activityLevel":        input["activityLevel"],
    "cuisines":             input["cuisines"],
    "medicalConditions":    input["medicalConditions"],
    "tastePreferences":     input["tastePreferences"],
    "specialization":       input["specialization"],
    "professionalStatement":  input["professionalStatement"],
    "availability":           input["availability"]
  }
  try:
    user = User.objects.get(username=username)
    print(user)
    # print("hello")
    user.first_name           = user_firstname
    user.last_name            = user_lastname
    user.age                  = clean_input["age"]
    user.gender               = clean_input["gender"]
    user.role                 = clean_input["role"]
    user.dietary_preference   = clean_input["dietaryPreference"]
    user.health_goal          = clean_input["healthGoal"]
    user.allergens            = clean_input["allergens"]
    user.activity_level       = clean_input["activityLevel"]
    user.cuisines             = clean_input["cuisines"]
    user.medical_conditions   = clean_input["medicalConditions"]
    user.taste_preferences    = clean_input["tastePreferences"]
    user.save()
    
    return {
      "message": "User On-boarded",
      "user": user
    }
  except User.DoesNotExist as error:
    return {
      "error": str(error)
    }


# def resolve_createUser(*_, input: dict):
#   clean_input = {
#     "first_name": input["first_name"], 
#     "last_name": input["last_name"], 
#     "email": input["email"], 
#     "username": input["username"],
#     "password": input["password"], 
#   }
#   try:
#     user = User.objects.create(first_name=clean_input["first_name"], last_name=clean_input["last_name"], email=clean_input["email"], username=clean_input["username"], password=clean_input["password"])
#     user.save()
#     return {
#       "message": "User Created",
#       "user": user
#     }
#   except ValueError as error:
#     return {
#       "error": str(error)
#     }


# def resolve_users(*_):
#   users = User.objects.all()
#   return {
#     "message": "Registered Users",
#     "users": users
#   }