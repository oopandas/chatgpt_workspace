from django.shortcuts import render, get_object_or_404
from .models import ChatLogModel
from django.views.generic import CreateView
from django.urls import reverse_lazy
from pathlib import Path
import json, tempfile, os, zipfile
from django.conf import settings
from datetime import datetime
from collections import defaultdict

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

def extract_json_from_zip(zip_file):
    """zipからjsonを抽出"""

    data = None
    #ここの文字列何入れるか迷う
    with zipfile.ZipFile(zip_file) as zip_ref:
        # temp_dirでデータを一時的に保存されるランダムなフォルダを作成する
        with tempfile.TemporaryDirectory() as temp_dir:
            # zipの中身をtemp_dirフォルダに全部取り出す
            zip_ref.extractall(temp_dir)

            print("Extracted files:")
            # zipの中に入っているファイルを一つずつ取り出して表示する
            for file in zip_ref.namelist():
                print(file)
                if "conversations.json" in file:
                    logs_path = os.path.join(temp_dir, file)
                
                    with open(logs_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        break  # conversations.jsonが見つかったらループを抜ける
    return data

def parse_conversations(data):
    """conversations.jsonの内容を解析して、会話のタイトルと日付ごとに会話の内容に整形"""
    
    # conversation_path = settings.BASE_DIR / "logs_data" / "conversations.json"

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
    return conversations

def upload_zip(request):
    """zipファイルをアップロードして、conversations.jsonの内容を解析して表示する"""
    # 最初に開いたとき
    if request.method == "GET":
        return render(request, "logs/upload_zip.html")
    
    # アップロードされたとき
    if request.method == "POST":
        zip_file = request.FILES.get("zip_file")

        if not zip_file:
            return render(request, "logs/upload_zip.html", {"error": "zipファイルを選択してください"})

        data = extract_json_from_zip(zip_file)

        if not data:
            return render(request, "logs/upload_zip.html", {"error": "conversations.jsonが見つかりませんでした"})

        conversations = parse_conversations(data)
    
        # 結果表示
        return render(request, "logs/import_json.html", {
            "data": {
                title: {date: logs for date, logs in dates.items()}
                for title, dates in conversations.items()
            }
        }) 




# Create your views here.
