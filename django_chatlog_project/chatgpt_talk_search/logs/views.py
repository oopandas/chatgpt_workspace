from django.shortcuts import render, get_object_or_404
from .models import ChatLogModel
from django.views.generic import CreateView
from django.urls import reverse_lazy
from pathlib import Path
import json
from django.conf import settings
from datetime import datetime
from collections import defaultdict
from zipfile import ZipFile

def logs_view(request):
    logs = ChatLogModel.objects.all()
    return render(request, "logs/index.html", {"logs": logs})

def logs_list(request):
    logs = ChatLogModel.objects.all()
    return render(request, "logs/logs_list.html", {"logs": logs})

def logs_detail(request, pk):
    logs = get_object_or_404(ChatLogModel, pk=pk)
    return render(request, "logs/logs_detail.html", {"logs": logs})

class LogsCreate(CreateView):
    template_name = "logs/logs_create.html"
    model = ChatLogModel
    fields = ("title", "content")
    success_url = reverse_lazy("logs:logs_list")

def import_json(request):
    print("ここ通っている")
    # conversation.jsonを変数に格納
    conversation_path = settings.BASE_DIR / "logs_data" / "conversations.json"

    # open関数でconversation.jsonを読み込み変数に格納
    with open(conversation_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conversations = defaultdict(lambda: defaultdict(list))
        
    for item in data:
        title = item.get("title")
        create_time = item.get("create_time")
        # print(create_time)
        logs_datetime = datetime.fromtimestamp(create_time)

        strftime = logs_datetime.strftime("%-m/%-d")  

        mapping = item.get("mapping", {})
        for value in mapping.values():
            message = value.get("message", {})
            if message:
                # 自分の会話だけ取得する意図
                author = message.get("author", {})
                role = author.get("role", "")
                if role == "user":
                    #ログの中身を掘っていく
                    content = message.get("content")
                    if content:
                        parts = content.get("parts", [])
                        parts_text = "\n".join(parts)
    
                        conversations[title][strftime].append(parts_text)
                        # print(conversations)

    return render(request, "logs/import_json.html", {
        "data": {
            title: {date: logs for date, logs in dates.items()}
            for title, dates in conversations.items()
        }
    }) 
    
def upload_zip(request):

    #ここの文字列何入れるか迷う
    with zipfile.ZipFile("file.zip") as zip_ref:
        zip_ref.extractall()
        print("Extracted files:")
        for file in zip_ref.namelist():
        print(file)
    


# Create your views here.
