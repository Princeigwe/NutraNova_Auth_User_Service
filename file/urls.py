from django.urls import path
from .views import upload_image_to_cloudinary

urlpatterns = [
  # path('upload/', upload_file, name='file-upload'),
  path('upload/', upload_image_to_cloudinary, name='image-upload'),
]