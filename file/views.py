from .serializers import CloudinaryUploadSerializer
from drf_spectacular.utils import extend_schema
from threads.upload_image_thread import UploadImageThread
import mimetypes
from django.http import HttpResponse
from django.core import serializers
import json
from utils.emit_profile_image_update import emit_profile_image
from rest_framework import status
from utils.jwt_encode_decode import decode_access_token
from celery import shared_task
from rest_framework.exceptions import ParseError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from utils.upload_image import upload_and_get_image_details
import os
from dotenv import load_dotenv
load_dotenv()


# Create your views here.


@extend_schema(request=CloudinaryUploadSerializer)
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
        if file_size > 3000000:  # (3MB)
            raise ParseError("Image too large")

        # cloudinary does not work properly with files with gaps in it. example, default screenshots names
        # checking for gaps in the file name
        elif any(char.isspace() for char in request_file.name):
            # raise ParseError("Image name cannot be parsed. Rename it or choose another")
            request_file.name = request_file.name.replace(' ', '_')

        # setting file storage location to /media/ folder in Vercel's temporary /tmp/ folder if API not running in development environment
        # default_storage = "/tmp/media/" if settings.ENVIRONMENT in ["production", "staging"] else settings.MEDIA_ROOT
        default_storage = settings.MEDIA_ROOT  # removed vercel tmp file storage
        fs = FileSystemStorage(location=default_storage)
        file = fs.save(request_file.name, request_file)
        file_url = fs.url(file)  # /media/<image>

        # setting image path to /tmp/media/<image> if API is running on Vercel environment
        # removed vercel file storage
        image_path = f"{settings.BASE_DIR}{file_url}"
        print(f"image path: {image_path}")

        image_mime_type, _ = mimetypes.guess_type(image_path)
        if image_mime_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise ParseError(
                "Please upload image with extensions .png or .jpeg")

        # uploading image in background thread
        upload_image_thread = UploadImageThread(image_path, user_email)
        upload_image_thread.start()  # run thread

        return Response({"message": "Profile image updated"}, status=status.HTTP_201_CREATED)
