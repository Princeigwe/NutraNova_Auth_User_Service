import pytest
import requests

def test_upgrade_profile(mock_post, user_json_response):
  mock_post.json.return_value = user_json_response
  response = requests.post('http://127.0.0.1:8000/graphql/', data={
    "query": '''mutation UpdateProfile { updateProfile( input: {
    age: 29
    gender:MALE,
    dietary_preference: DAIRY_FREE,
    health_goal:WEIGHT_LOSS,
    activity_level: LIGHTLY_ACTIVE,
    cuisines: [INDIAN, ASIAN],
    allergens: [MILK],
    medical_conditions: [PREGNANCY],
    professional_statement: "Hello world, I'm a chef"
    availability:false,
    taste_preferences:[AROMATIC, SOUR],
  } ){
    firstName
    lastName
    email
    username
    age
    gender
    role
    dietaryPreference
    healthGoal
    allergens
    cuisines
    activityLevel
    professionalStatement
    availability
    medicalConditions
    tastePreferences
  } 
  }''',
  "operationName": "UpdateProfile"
  })
  assert response.json() == user_json_response
