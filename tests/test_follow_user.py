import pytest
import requests

def test_follow_user(mock_post, follow_user_response):
  mock_post.json.return_value = follow_user_response
  response = requests.post('http://127.0.0.1:8000/graphql', data={
    "query": '''
            mutation FollowUser {
              followUser(username:"thebestcook"){
                message
              }
            }
    ''', 
    "operationName": "FollowUser"
  })
  assert response.json() == follow_user_response