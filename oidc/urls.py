from django.urls import path 
from .views import oidc_authenticate, oidc_callback

urlpatterns = [
  path('auth/', oidc_authenticate),
  path('callback/', oidc_callback)
]