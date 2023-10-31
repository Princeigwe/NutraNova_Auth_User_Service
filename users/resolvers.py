from utils.jwt_encode_decode import decode_access_token
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from utils.get_token_email import get_user_email
from .models import UserFollowing

User = get_user_model()

@database_sync_to_async
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


@database_sync_to_async
def resolve_update_profile(_, info, input:dict):
  user_email = get_user_email(info)

  try:
    user = User.objects.get(email=user_email)
    if user.role == "USER" and ('specialization' in input):
      raise Exception("Invalid action: Cannot set specialization with USER role.")

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


@database_sync_to_async
def resolve_update_username(_, info, input:dict):
  user_email = get_user_email(info)

  desired_username = input['username']
  results = User.objects.filter(username=input['username'])
  if len(results) != 0:
    raise Exception(f"{desired_username} is already taken")
  
  try:
    user = User.objects.get(email=user_email)
    user.username = input['username']
    user.save()
    return user
  except User.DoesNotExist:
    raise Exception("User does not exist")


@database_sync_to_async
def resolve_get_user(*_, username):
  try:
    user = User.objects.get(username=username)
    return user
  except User.DoesNotExist:
    raise Exception("User not found")


@database_sync_to_async
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
    raise Exception("Invalid Action")
  
  except UserFollowing.DoesNotExist:
    user_following = UserFollowing.objects.create(user_id=current_user, following_user_id=user_to_follow)
    user_following.save()
    return {
      "message": f"You are now following {user_to_follow.username}"
    }



@database_sync_to_async
def resolve_get_my_followers():
  pass


@database_sync_to_async
def resolve_get_my_followings():
  pass


@database_sync_to_async
def resolve_get_user_followers():
  pass


@database_sync_to_async
def resolve_get_user_followings():
  pass





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