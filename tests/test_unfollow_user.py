import pytest
import requests


def test_unfollow_user(mock_post, un_follow_user_response):
  mock_post.json.return_value = un_follow_user_response
  response = requests.post('http://127.0.0.1:8000/graphql', data={
    "query": '''
            mutation UnFollowUser {
              unFollowUser(username:"thebestcook"){
                message
              }
            }
    ''', 
    "operationName": "UnFollowUser"
  })
  assert response.json() == mock_post.json.return_value