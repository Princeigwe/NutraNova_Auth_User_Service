from django.shortcuts import render, redirect
import requests
from dotenv import load_dotenv
import os
from django.http import JsonResponse

auth0_domain = os.environ.get("AUTH0_DOMAIN")
client_id = os.environ.get('AUTH0_CLIENT_ID')
client_application_domain = os.environ.get('CLIENT_APPLICATION_DOMAIN')

def oidc_authenticate(request):
  auth0_authorize_url = f'https://{auth0_domain}/authorize'
  redirect_uri = f"http://{client_application_domain}/oidc/callback/"

  params = {
      "response_type": "code",
      "client_id": client_id,
      "redirect_uri": redirect_uri,
      "scope": "openid profile email",
  }

  return redirect( f"{auth0_authorize_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}" )

def oidc_callback(request):
  authorization_code = request.GET.get("code")
  redirect_uri = f"http://{client_application_domain}/oidc/callback/"

  # exchanging code for token
  token_url = f'https://{auth0_domain}/oauth/token'
  token_data = {
      "grant_type": "authorization_code",
      "client_id": client_id,
      "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
      "code": authorization_code,
      "redirect_uri": redirect_uri
  }

  try:
    token_response = requests.post(token_url, data=token_data)
    token_response_data = token_response.json()
  except requests.exceptions.ConnectionError as e:
    print ( f'Connection Error: {e}' )
  except requests.exceptions.Timeout:
    print (f'Timeout Error: {e}')
  

  # retrieve authenticated user details
  if "access_token" in token_response_data:
    access_token = token_response_data['access_token']
    user_info_url = f'https://{auth0_domain}/userinfo'

    params = {
        "access_token": access_token
    }

    try:
      response = requests.get(user_info_url, params=params)
      user_info_response_data = response.json()
      return JsonResponse(user_info_response_data)
    except requests.exceptions.ConnectionError as e:
      print ( f'Connection Error: {e}' )
    except requests.exceptions.Timeout:
      print (f'Timeout Error: {e}')
