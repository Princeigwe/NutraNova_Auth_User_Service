import requests
from dotenv import load_dotenv
import os
load_dotenv()


import cloudinary
import cloudinary.uploader
import cloudinary.api


cloudinary.config(
  cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
  api_key = os.environ.get("CLOUDINARY_API_KEY"),
  api_secret = os.environ.get("CLOUDINARY_API_SECRET")
)


# uploading image 
def upload_image(file):
  cloudinary.uploader.upload(file, use_filename = True, unique_filename = False)
  srcURL = cloudinary.CloudinaryImage(file).build_url()
  return srcURL


# fetching image info 
def upload_and_get_image_details(file):
  built_image = upload_image(file)
  image_name = os.path.basename(built_image)

  # getting the name of image from its extension. this is what is used as the public id of uploaded image in cloudinary
  image_public_id, extension = os.path.splitext(image_name)
  print(image_name)
  image_info = cloudinary.api.resource(image_public_id)

  # removed file at this spot, because the self upload_and_get_image_details function will not be running as a demonic thread.
  # meaning that the file which is needed for upload can be deleted from container's media folder before the function is called,
  # thereby throwing an error 
  os.remove(file)
  if os.path.exists(file):
    print('image exists')
  else:
    print('image does not exist')

  return image_info