import pytest
import requests

def test_my_followers(mock_post, my_followers_json_response):
  mock_post.json.return_value = my_followers_json_response
  response = requests.post('http://127.0.0.1:8000/graphql/', data={
    "query": '''
            query MyFollowers {
              myFollowers {
                number
                users {
                  username
                }
              }
            }
      ''',
    "operationName": "MyFollowers"
  })
  assert response.json() == my_followers_json_response
