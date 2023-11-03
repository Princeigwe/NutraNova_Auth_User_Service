from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from utils.upload_image import upload_image, upload_and_get_image_details
from django.http import HttpRequest
import os
from dotenv import load_dotenv
load_dotenv()
import time
import datetime
import cloudinary
import requests
from django.core.files .storage import FileSystemStorage
from django.conf import settings
from pathlib import Path

# Create your views here.


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_image_to_cloudinary(request):
  request_file = request.FILES['image'] if 'image' in request.FILES else None
  current_directory = os.getcwd()

  print(current_directory)

  if request_file:
    fs = FileSystemStorage()
    file = fs.save(request_file.name, request_file)
    file_url = fs.url(file)
    image_path = f"{settings.BASE_DIR}{file_url}"

    print(image_path)
    print(settings.BASE_DIR)


    # upload = upload_image( image_path )
    upload = upload_and_get_image_details(image_path)
    current_directory = os.getcwd()
    return Response(upload)




def cloudinary_authentication_signature():
  current_time = datetime.datetime.now()
  current_year = current_time.year
  current_month = current_time.month
  current_day = current_time.day
  current_hour = current_time.hour
  current_minute = current_time.minute

  date_time = datetime.datetime(current_year, current_month, current_day, current_hour, current_minute)
  unix_timestamp = time.mktime(date_time.timetuple())
  timestamp = unix_timestamp
  
  params_to_sign = {"timestamp": timestamp}

  api_secret = os.environ.get("CLOUDINARY_API_SECRET")
  signature = cloudinary.utils.api_sign_request(params_to_sign, api_secret)
  return unix_timestamp, signature



@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_file(request: HttpRequest):
  if 'file' not in request.data:
    return Response({'error': 'No file part found'}, status=status.HTTP_BAD_REQUEST)
  
  file = request.FILES.get('file')
  resource_type="image"
  cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
  api_key = os.environ.get("CLOUDINARY_API_KEY")
  unix_timestamp, signature = cloudinary_authentication_signature()


  # url = f"https://api.cloudinary.com/{cloud_name}/{resource_type}/upload"
  url = f"https://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload"
  data = {
    "file": file,
    "api_key": api_key,
    "timestamp": unix_timestamp,
    "signature": signature
  }
  r = requests.post(url, data)
  if r.status_code == 200:
    response = r.json()
    return Response(response)
  else:
    print(file.size)
    print(request.content_type)
    print("Error from server: " + str(r.content))
    return Response(r.json())