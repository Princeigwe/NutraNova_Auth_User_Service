import os
import jwt
from datetime import datetime, timedelta

secret_key = os.environ.get('JWT_SECRET_KEY')
nutra_nova_api_domain = os.environ.get('NUTRANOVA_AUTH_API_DOMAIN')

def encode_access_token(payload: dict):
  payload["iss"] = nutra_nova_api_domain
  payload["iat"] = datetime.utcnow()
  payload["exp"] = datetime.utcnow() + timedelta(days=1)
  encoded_data = jwt.encode(payload=payload, key=secret_key, algorithm="HS256")
  return encoded_data


def decode_access_token(token):
  try:
    decoded_data = jwt.decode(jwt=token, key=secret_key, algorithms=["HS256"])
    return decoded_data
  except jwt.ExpiredSignatureError as e:
    message = f'Invalid token: {e}'
    return message