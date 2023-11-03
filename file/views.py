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


