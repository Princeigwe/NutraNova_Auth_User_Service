from utils.jwt_encode_decode import decode_access_token
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from utils.get_token_email import get_user_email
from .models import UserFollowing
from utils.kafka.produce.update_username_chef import send_updated_username
from utils.jwt_encode_decode import encode_access_token


User = get_user_model()

# commented out all database_sync_to_async decorator because I discovered Vercel does not support websocket connection for Daphne Channels

# @database_sync_to_async
def resolve_onboard_user(_, info, input:dict):

  # request = info.context["request"] # get http request from info.context
  # authorization_header = request.headers.get("Authorization") # retrieve Authorization header to fetch value
  # parts = authorization_header.split(" ") # split value by the space
  # token = parts[1] # get the token
  # decoded_data = decode_access_token(token) # decode token
  # user_email = decoded_data['email']

  user_email = get_user_email(info)


  if input['role'] == "USER" and ('specialization' in input):
    raise Exception("Invalid action: Cannot set specialization with USER role.")

  try:
    user = User.objects.get(email=user_email)
    if user.is_on_boarded:
      raise Exception( "User is already on-boarded. Update profile to make changes." )
    user.age = input['age']
    user.gender = input['gender']
    user.role = input['role']
    user.dietary_preference = input['dietary_preference']
    user.health_goal = input['health_goal']
    user.activity_level = input['activity_level']
    user.cuisines = input['cuisines']
    user.taste_preferences = input['taste_preferences']
    user.is_on_boarded = True

    # optional input fields
    if 'allergens' in input:
      user.allergens = input['allergens']
    if 'medical_conditions' in input:
      user.medical_conditions = input['medical_conditions']
    if 'specialization' in input:
      user.specialization = input['specialization'] 
    if 'professional_statement' in input:
      user.professional_statement = input['professional_statement']
    if 'availability' in input:
      user.availability = input['availability']
    
    user.save()
    return user
  except User.DoesNotExist:
    print('User does not exist')
    raise Exception('User does not exist')


# @database_sync_to_async
def resolve_update_profile(_, info, input:dict):
  """
  The function `resolve_update_profile` updates the profile of a user, checking for certain conditions
  and saving the changes.
  """
  user_email = get_user_email(info)

  try:
    user = User.objects.get(email=user_email)
    if user.role == "USER" and ('specialization' in input):
      raise Exception("Invalid action: Cannot set specialization with USER role.")

    # The code block is iterating over the key-value pairs in the `input` dictionary. It checks if the
    # value is not None and if the keys `'cuisines'` and `'taste_preferences'` are present in the
    # `input` dictionary. If both conditions are true, it sets the attribute of the `user` object with
    # the corresponding key to the value.
    for key, value in input.items():
      if value is not None:
        if 'cuisines' in input :
          if len(input['cuisines']) != 0:
            if 'taste_preferences' in input:
              if len(input['taste_preferences']) != 0:
                setattr(user, key, value)
    
    user.save()
    return user
  except User.DoesNotExist:
    print('User does not exist')
    raise Exception('User does not exist')


# @database_sync_to_async
def resolve_update_username(_, info, input:dict):
  user_email = get_user_email(info)

  desired_username = input['username']
  results = User.objects.filter(username=input['username'])
  if len(results) != 0:
    raise Exception(f"{desired_username} is already taken")
  
  try:
    user = User.objects.get(email=user_email)
    old_username = user.username
    user.username = input['username']
    user.save()

    # send message to kafka
    kafka_message = {
      "old_username": old_username,
      "new_username": user.username # updated username
    }

    send_updated_username(kafka_message)

    # create new access token for user of updated username
    payload = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "gender": user.gender,
        "role": user.role,
        "dietary_preference": user.dietary_preference,
        "taste_preferences": user.taste_preferences,
        "health_goal": user.health_goal,
        "allergens": user.allergens,
        "activity_level": user.activity_level,
        "cuisines": user.cuisines,
        "medical_conditions": user.medical_conditions,
        "is_on_boarded": user.is_on_boarded,
    }
    jwt = encode_access_token(payload)
    return {
      "user": user, 
      "jwt": jwt
    }
  except User.DoesNotExist:
    raise Exception("User does not exist")


# @database_sync_to_async
def resolve_get_user(*_, username):
  try:
    user = User.objects.get(username=username)
    return user
  except User.DoesNotExist:
    raise Exception("User not found")


# @database_sync_to_async
def resolve_get_my_profile(_, info):
  user_email = get_user_email(info)
  try:
    current_user = User.objects.get(email=user_email)
    return current_user
  except User.DoesNotExist:
    raise Exception("User not found")

# @database_sync_to_async
def resolve_follow_user(_, info, username):
  user_email = get_user_email(info)
  try:
    user_to_follow = User.objects.get(username=username)
    current_user = User.objects.get(email=user_email)
    UserFollowing.objects.get(user_id=current_user, following_user_id=user_to_follow)
    return {
      "message": f"You already follow {user_to_follow.username}"
    }
  
  except User.DoesNotExist:
    raise Exception("Invalid Action: User does not exist")
  
  except UserFollowing.DoesNotExist:
    user_following = UserFollowing.objects.create(user_id=current_user, following_user_id=user_to_follow)
    user_following.save()
    return {
      "message": f"You are now following {user_to_follow.username}"
    }


def resolve_un_follow_user(_, info, username):
  user_email = get_user_email(info)
  try:
    current_user = User.objects.get(email=user_email)
    user_followed = User.objects.get(username=username)
    user_following = UserFollowing.objects.get(user_id=current_user, following_user_id=user_followed)
    user_following.delete()
    return {
      "message": f"You unfollowed {username}"
    }
  except UserFollowing.DoesNotExist:
    return None


# @database_sync_to_async
def resolve_my_followers(_, info):
    user_email = get_user_email(info)
    try:
      follower_list = []
      user = User.objects.prefetch_related("followers").get(email=user_email)
      user_followers = user.followers.all() # fetch the UserFollowing objects related to the user 
      for follower in user_followers:
        follower_list.append(
          {
            "username": follower.user_id.username,
            "professional_statement": follower.user_id.professional_statement
          }
        )
      number_of_followers = len(follower_list)
      # return follower_list
      return {
        "number": number_of_followers,
        "users": follower_list
      }
    
    except User.DoesNotExist:
      raise Exception("User does not exist")


# @database_sync_to_async
def resolve_my_following(_, info):
  user_email = get_user_email(info)
  try:
    following_list = []
    user = User.objects.prefetch_related("following").get(email=user_email)
    user_following = user.following.all()
    for follow in user_following:
      following_list.append(
        {
          "username": follow.following_user_id.username,
          "professional_statement": follow.following_user_id.professional_statement
        }
      )
    # return following_list
    number_of_followings = len(following_list)
    return {
      "number": number_of_followings,
      "users": following_list
    }
  except User.DoesNotExist:
    raise Exception("User does not exist")


# @database_sync_to_async
def resolver_user_followers(_, info, username):
  follower_list = []
  try:
    user = User.objects.prefetch_related("followers").get(username=username)
    user_followers = user.followers.all()
    for follower in user_followers:
      follower_list.append(
        {
          "username": follower.user_id.username,
          "professional_statement": follower.user_id.professional_statement
        }
      )
    # return follower_list
    number_of_followers = len(follower_list)
    return {
        "number": number_of_followers,
        "users": follower_list
    }
  
  except User.DoesNotExist:
    raise Exception("User does not exist")


# @database_sync_to_async
def resolve_user_following(_, info, username):
  try:
    following_list = []
    user = User.objects.prefetch_related("following").get(username=username)
    user_following = user.following.all()
    for follow in user_following:
      following_list.append(
        {
          "username": follow.following_user_id.username,
          "professional_statement": follow.following_user_id.professional_statement
        }
      )
    # return following_list
    number_of_followings = len(following_list)
    return {
      "number": number_of_followings,
      "users": following_list
    }
  except User.DoesNotExist:
    raise Exception("User does not exist")




def resolve_password_with_permission_check(obj, info):
  current_user_email = get_user_email(info)
  if current_user_email == obj.email:
    return obj.password
  return None


def resolve_medical_conditions_with_permission_check(obj, info):
  current_user_email = get_user_email(info)
  if current_user_email == obj.email:
    return obj.medical_conditions
  return None