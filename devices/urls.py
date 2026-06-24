from django.urls import path
from .views import list_devices

urlpatterns = [
    path("", list_devices),
]