import pytest
from django.contrib.auth import get_user_model
import requests

User = get_user_model()


# mocking POST request of requests package
@pytest.fixture()
def mock_post(mocker):
  mock = mocker.Mock()
  mocker.patch("requests.post", return_value=mock)
  return mock


@pytest.fixture()
def user_json_response():
  response = {
  "data": {
    "updateProfile": {
      "firstName": "test",
      "lastName": "user",
      "email": "testuser@gmail.com",
      "username": "testuser",
      "age": 29,
      "gender": "MALE",
      "role": "USER",
      "dietaryPreference": "DAIRY_FREE",
      "healthGoal": "WEIGHT_LOSS",
      "allergens": [
        "MILK"
      ],
      "cuisines": [
        "INDIAN",
        "ASIAN"
      ],
      "activityLevel": "LIGHTLY_ACTIVE",
      "professionalStatement": "Hello world, I'm a chef",
      "availability": False,
      "medicalConditions": [
        "PREGNANCY"
      ],
      "tastePreferences": [
        "AROMATIC",
        "SOUR"
      ]
    }
  }
}
  return response


@pytest.fixture()
def my_followers_json_response():
  response = {
    "data": {
      "myFollowers": {
        "number": 1,
        "users": [
          {
            "username": "thebestcook",
            "professionalStatement": "Hello world, I'm a chef"
          }
        ]
      }
    }
  }
  return response


@pytest.fixture()
def follow_user_response():
  response = {
    "data": {
      "followUser": {
        "message": "You are now following thebestcook"
      }
    }
  }
  return response


@pytest.fixture()
def un_follow_user_response():
  response = {
    "data": {
      "unFollowUser": {
        "message": "You unfollowed thebestcook"
      }
    }
  }
  return response

@pytest.fixture()
def my_following_json_response():
  response = {
    "data": {
      "myFollowing": {
        "number": 1,
        "users": [
          {
            "username": "thebestcook",
            "professionalStatement": "Hello world, I'm a chef"
          }
        ]
      }
    }
  }
  return response



@pytest.fixture()
def user():
  return {
      "firstName": "test",
      "lastName": "user",
      "email": "testuser@gmail.com",
      "username": "testuser",
      "age": 29,
      "gender": "MALE",
      "role": "USER",
      "dietaryPreference": "DAIRY_FREE",
      "healthGoal": "WEIGHT_LOSS",
      "allergens": [
        "MILK"
      ],
      "cuisines": [
        "INDIAN",
        "ASIAN"
      ],
      "activityLevel": "LIGHTLY_ACTIVE",
      "professionalStatement": "Hello world, I'm a chef",
      "availability": False,
      "medicalConditions": [
        "PREGNANCY"
      ],
      "tastePreferences": [
        "AROMATIC",
        "SOUR"
      ]
  }