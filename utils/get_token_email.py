from .jwt_encode_decode import decode_access_token

def get_user_email(info):
  request = info.context["request"] # get http request from info.context
  authorization_header = request.headers.get("Authorization") # retrieve Authorization header to fetch value
  parts = authorization_header.split(" ") # split value by the space
  token = parts[1] # get the token
  decoded_data = decode_access_token(token) # decode token
  user_email = decoded_data['email']
  return user_email