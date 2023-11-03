from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from utils.upload_image import upload_and_get_image_details
import os
from dotenv import load_dotenv
load_dotenv()
from django.core.files .storage import FileSystemStorage
from django.conf import settings
from rest_framework.exceptions import ParseError
import magic  # for reading file mimetype

# Create your views here.


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_image_to_cloudinary(request):
  request_file = request.FILES['image'] if 'image' in request.FILES else None
  current_directory = os.getcwd()

  print(current_directory)

  if request_file:

    # cloudinary does not work properly with files with gaps in it. example, default screenshots names 
    if any( char.isspace() for char in request_file.name): # checking for gaps in the file name
      raise ParseError("Image name cannot be parsed. Rename it or choose another")

    fs = FileSystemStorage()
    file = fs.save(request_file.name, request_file)
    file_url = fs.url(file)
    image_path = f"{settings.BASE_DIR}{file_url}"

    image_mime_type = magic.from_file(image_path, mime=True)
    if image_mime_type != "image/jpeg" or "image/png":
      raise ParseError("Please upload image with extensions .png or .jpeg")

    print(image_path)
    print(settings.BASE_DIR)


    # upload = upload_image( image_path )
    upload = upload_and_get_image_details(image_path)
    current_directory = os.getcwd()
    return Response(upload)


