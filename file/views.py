from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from utils.upload_image import upload_and_get_image_details
import os
from dotenv import load_dotenv
load_dotenv()
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.exceptions import ParseError
from celery import shared_task
from utils.jwt_encode_decode import decode_access_token
from rest_framework import status
from users.tasks import set_profile_image
import json
from django.core import serializers
from django.http import HttpResponse
import mimetypes


# Create your views here.


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_image_to_cloudinary(request):
  """
  The function `upload_image_to_cloudinary` uploads an image file to Cloudinary, validates the file
  size and name, checks the file type, and updates the user's profile image with the uploaded image.
  """
  authorization_header = request.headers.get("Authorization") 
  if not authorization_header:
    return Response({"message": "Unauthorized request"}, status=status.HTTP_400_BAD_REQUEST)
  parts = authorization_header.split(" ")
  token = parts[1] 
  decoded_data = decode_access_token(token) 
  user_email = decoded_data['email']

  request_file = request.FILES['image'] if 'image' in request.FILES else None
  # current_directory = os.getcwd()
  # print(current_directory)
  if request_file:

    file_size = request_file.size
    if file_size > 3000000: #(3MB)
      raise ParseError("Image too large")

    # cloudinary does not work properly with files with gaps in it. example, default screenshots names 
    elif any( char.isspace() for char in request_file.name): # checking for gaps in the file name
      raise ParseError("Image name cannot be parsed. Rename it or choose another")

    # setting file storage location to /media/ folder in Vercel's temporary /tmp/ folder if API not running in development environment
    default_storage = "/tmp/media/" if settings.ENVIRONMENT in ["production", "staging"] else settings.MEDIA_ROOT
    fs = FileSystemStorage(location=default_storage)
    file = fs.save(request_file.name, request_file)
    file_url = fs.url(file)
    image_path = f"{settings.BASE_DIR}{file_url}"

    image_mime_type, _ = mimetypes.guess_type(image_path)
    if image_mime_type not in ["image/jpeg", "image/png", "image/jpg"]:
      raise ParseError("Please upload image with extensions .png or .jpeg")

    upload = upload_and_get_image_details(image_path)
    user = set_profile_image(upload["secure_url"], user_email)
    serialized_user = serializers.serialize('json', [user, ])
    response = {
        "user": serialized_user
    }
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type='application/json')