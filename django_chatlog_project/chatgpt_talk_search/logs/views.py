from django.shortcuts import render, get_object_or_404
from .models import ChatLogModel
from django.views.generic import CreateView
from django.urls import reverse_lazy
from pathlib import Path
import json
from django.conf import settings


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
    # conversation.jsonを変数に格納
    conversation_path = settings.BASE_DIR / "logs_data" / "conversations.json"

    # open関数でconversation.jsonを読み込み変数に格納
    with open(conversation_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conversations = []
        
    for item in data:
        title = item.get("title")
        create_time = item.get("create_time")
        update_time = item.get("update_time")

        mapping = item.get("mapping", {})
        for value in mapping.values():
            message = value.get("message")

            if message:
                content = message.get("content")
                if content:
                    parts = content.get("parts", [])

                    conversations.append({
                        "title": title,
                        "create_time": create_time,
                        "update_time": update_time,
                        "parts": parts,
            
                    })

    return render(request, "logs/import_json.html", {"data": conversations}) 



# Create your views here.
