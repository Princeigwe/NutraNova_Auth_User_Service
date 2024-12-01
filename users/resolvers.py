from utils.jwt_encode_decode import decode_access_token
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from utils.get_token_email import get_user_email
from .models import UserFollowing
from utils.rabbitmq.publishers.user_data_update import send_user_data_update as rabbitmq_update
from utils.jwt_encode_decode import encode_access_token
from utils.update_access_token import update_access_token
from .views import oidc_get_or_create_user


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
      updated_access_token = update_access_token(user)
      raise Exception( f"User is already on-boarded, update profile to make changes. New access token: {updated_access_token} " )
    user.dob = input['dob']
    user.telephone = input['telephone']
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

    # if user is onboarding as a regular user, they cannot input specializations meant for health experts
    if (input['role'] == 'USER') and ('specialization' in input):
      raise Exception("Specialization of health experts cannot be used on individual user")

    if 'specialization' in input:
      user.specialization = input['specialization'] 
    if 'professional_statement' in input:
      user.professional_statement = input['professional_statement']
    if 'availability' in input:
      user.availability = input['availability']
    
    user.save()
    jwt = update_access_token(user)
    # return user
    return {
      "user": user, 
      "jwt": jwt
    }

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
    
    user.first_name             = input['first_name'] if 'first_name' in input else user.first_name
    user.last_name              = input['last_name'] if 'last_name' in input else user.last_name
    user.dob                    = input['dob'] if 'dob' in input else user.dob
    user.telephone                    = input['telephone'] if 'telephone' in input else user.telephone
    user.dietary_preference     = input['dietary_preference'] if 'dietary_preference' in input else user.dietary_preference
    user.health_goal            = input['health_goal'] if 'health_goal' in input else user.health_goal
    user.activity_level         = input['activity_level'] if 'activity_level' in input else user.activity_level
    user.cuisines               = input['cuisines'] if 'cuisines' in input else user.cuisines
    user.taste_preferences      = input['taste_preferences'] if 'taste_preferences' in input else user.taste_preferences

    user.specialization         = input['specialization'] if 'specialization' in input else user.specialization
    user.professional_statement = input['professional_statement'] if 'professional_statement' in input else user.professional_statement
    user.availability           = input['availability'] if 'availability' in input else user.availability
    
    user.save()
    jwt = update_access_token(user)

    # send message to kafka
    event_message = {
      # general data needed for all microservices
      "username": user.username,
      "first_name": user.first_name,
      "last_name": user.last_name,

      # specific data needed for the user foreign key in recipe model in Recipe microservice
      # user_image is supposed is supposed to be among, but that is handled in the microservice REST API endpoint for uploading image
      "vote_strength": user.vote_strength,
      "is_verified": user.is_verified,

      # specific data needed for the user preferences in Chef model in Recommendations microservice
      "preferences": {
        "dietary_preference": user.dietary_preference,
        "health_goal":        user.health_goal,
        "allergens":          user.allergens,
        "activity_level":     user.activity_level,
        "cuisines":           user.cuisines,
        "medical_conditions": user.medical_conditions,
        "taste_preferences":  user.taste_preferences
      }
    }

    # publish updated user message to rabbitmq
    rabbitmq_update(event_message)

    return {
      "user": user, 
      "jwt": jwt
    }
  except User.DoesNotExist:
    print('User does not exist')
    raise Exception('User does not exist')


# @database_sync_to_async
def resolve_update_username(_, info, input:dict):
  user_email = get_user_email(info)

  desired_username = input['username']
  trimmed_desired_username = desired_username.strip()
  if (" " in trimmed_desired_username) or ("@" in trimmed_desired_username):
    raise Exception("Spaced characters and @ not allowed in username. Please try again.")
  results = User.objects.filter(username=input['username'])
  if len(results) != 0:
    raise Exception(f"{desired_username} is already taken")
  
  try:
    user = User.objects.get(email=user_email)
    old_username = user.username
    # user.username = input['username']
    user.username = trimmed_desired_username
    user.save()

    # send message to kafka
    event_message = {
      "old_username": old_username,
      "new_username": user.username, # updated username

    }

    # publish updated user message to rabbitmq
    rabbitmq_update(event_message)

    # create new access token for user of updated username 
    # in order for the user to interact properly with their
    # created recipes in the recipes service
    payload = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "dob": str(user.dob),
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