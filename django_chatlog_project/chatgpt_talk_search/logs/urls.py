from django.urls import path
from . import views

app_name = "logs"

urlpatterns = [
    path("upload_zip/", views.upload_zip, name="upload_zip"),
]
