from rest_framework import serializers

class CloudinaryUploadSerializer(serializers.Serializer):
  image = serializers.FileField(max_length=None, allow_empty_file=False)