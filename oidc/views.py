from django.shortcuts import render, redirect
import requests
from dotenv import load_dotenv
import os
from django.http import HttpResponse

auth0_domain = os.environ.get("AUTH0_DOMAIN")
client_id = os.environ.get('AUTH0_CLIENT_ID')
client_application_domain = os.environ.get('CLIENT_APPLICATION_DOMAIN')

def oidc_authenticate(request):
    auth0_authorize_url = f'https://{auth0_domain}/authorize'
    client_application_domain = os.environ.get('CLIENT_APPLICATION_DOMAIN')
    redirect_uri = "http://127.0.0.1:8000/oidc/callback/"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile",
    }

    # response = requests.get(url=auth0_authorize_url, params=params)
    return redirect( f"{auth0_authorize_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}" )

def oidc_callback(request):
    authorization_code = request.GET.get("code")
    client_application_domain = os.environ.get('CLIENT_APPLICATION_DOMAIN')
    redirect_uri = "http://127.0.0.1:8000/oidc/callback/"

    # exchanging code for token
    token_url = f'https://{auth0_domain}/oauth/token'
    token_data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }

    # response = requests.post(url=token_url, data=data)
    # response = response.json()
    token_response = requests.post(token_url, data=token_data)
    token_response_data = token_response.json()
    print(token_response_data)
    return HttpResponse("Authentication complete!")