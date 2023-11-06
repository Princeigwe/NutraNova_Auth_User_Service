import requests
from dotenv import load_dotenv
import os
load_dotenv()


import cloudinary
import cloudinary.uploader
import cloudinary.api

from celery import shared_task

cloudinary.config(
  cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
  api_key = os.environ.get("CLOUDINARY_API_KEY"),
  api_secret = os.environ.get("CLOUDINARY_API_SECRET")
)


# uploading image in background as celery task
@shared_task
def upload_image(file):
  cloudinary.uploader.upload(file, use_filename = True, unique_filename = False)
  srcURL = cloudinary.CloudinaryImage(file).build_url()
  return srcURL


# fetching image info in background as celery task
@shared_task
def upload_and_get_image_details(file):
  built_image = upload_image(file)
  image_name = os.path.basename(built_image)

  # getting the name of image from its extension. this is what is used as the public id of uploaded image in cloudinary
  image_public_id, extension = os.path.splitext(image_name)
  print(image_name)
  image_info = cloudinary.api.resource(image_public_id)
  return image_info