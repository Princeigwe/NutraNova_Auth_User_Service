import pytest
import requests


def test_my_following(mock_post, my_following_json_response):
  mock_post.json.return_value = my_following_json_response
  response = requests.post('http://127.0.0.1:8000/graphql/', data={
    "query": '''
            query MyFollowing {
              myFollowing {
                number
                users {
                  username
                }
              }
            }
      ''',
    "operationName": "MyFollowing"
  })
  assert response.json() == my_following_json_response