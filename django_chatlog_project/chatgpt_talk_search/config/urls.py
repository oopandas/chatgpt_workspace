from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # ルートURLにアクセスしたときにログアップロードページにリダイレクト
    path("", lambda request: redirect("logs:upload_zip")),  
    path("admin/", admin.site.urls),
    path("logs/", include("logs.urls")),
]
