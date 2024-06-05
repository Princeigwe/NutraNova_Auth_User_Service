from .jwt_encode_decode import encode_access_token


def update_access_token(user):
  """this is used to update the access token for a user for every change in profile data"""
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
    "specialization": user.specialization,
    "professional_statement": user.professional_statement,
    "availability": user.availability,
    "is_on_boarded": user.is_on_boarded,
    "vote_strength": user.vote_strength,
    "is_verified": user.is_verified
    }
  jwt = encode_access_token(payload)
  return jwt