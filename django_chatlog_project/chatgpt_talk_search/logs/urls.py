from django.urls import path
from . import views
from logs.views import LogsCreate

app_name = "logs"

urlpatterns = [
    path("", views.logs_view, name="logs"),
    path("list/", views.logs_list, name="logs_list"),
    path("detail/<int:pk>/", views.logs_detail, name="logs_detail"),
    path("create/", LogsCreate.as_view(), name="create"),
    path("upload_zip/", views.upload_zip, name="upload_zip"),
]
