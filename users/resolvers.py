from utils.jwt_encode_decode import decode_access_token
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from utils.get_token_email import get_user_email

User = get_user_model()

@database_sync_to_async
def resolve_onboardUser(_, info, input:dict):

  request = info.context["request"] # get http request from info.context
  authorization_header = request.headers.get("Authorization") # retrieve Authorization header to fetch value
  parts = authorization_header.split(" ") # split value by the space
  token = parts[1] # get the token
  decoded_data = decode_access_token(token) # decode token
  user_email = decoded_data['email']

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
def resolve_updateProfile(_, info, input:dict):
  user_email = get_user_email(info)

  try:
    user = User.objects.get(email=user_email)
    if user.role == "USER" and ('specialization' in input):
      raise Exception("Invalid action: Cannot set specialization with USER role.")

    for key, value in input.items():
      if value is not None:
        setattr(user, key, value) # set all attribute key value values of user to attribute key values of input
    user.save()
    return user
  except User.DoesNotExist:
    print('User does not exist')
    raise Exception('User does not exist')
