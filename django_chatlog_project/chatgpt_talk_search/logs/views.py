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

    conversations_data = []

    with zipfile.ZipFile(zip_file) as zip_ref:
        # temp_dirでデータを一時的に保存されるランダムなフォルダを作成する
        with tempfile.TemporaryDirectory() as temp_dir:
            # zipの中身をtemp_dirフォルダに全部取り出す
            zip_ref.extractall(temp_dir)

            print("Extracted files:")
            # zipの中に入っているファイルを一つずつ取り出して表示する
            for file in zip_ref.namelist():
                # print(file)
                # if "conversations.json" in file:
                if file.startswith("conversations") and file.endswith(".json"):
                    logs_path = os.path.join(temp_dir, file)
                
                    with open(logs_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        conversations_data.extend(data)
                        # break  # conversations.jsonが見つかったらループを抜ける
    return conversations_data

def parse_conversations(zip_data):
    """conversations.jsonの内容を解析して、会話のタイトルと日付ごとに会話の内容に整形"""
    
    # conversation_path = settings.BASE_DIR / "logs_data" / "conversations.json"

    # conversations = defaultdict(lambda: defaultdict(list))
    conversations = defaultdict(lambda: {
        "create_time": None,
        "logs_by_date": 
    defaultdict(list)})

        
    for item in zip_data:
        title = item.get("title")
        if not title:
            continue
        create_time = item.get("create_time")
        if not create_time:
            continue
        # print(create_time)
        # logs_datetime = datetime.fromtimestamp(create_time)

        # strftime = logs_datetime.strftime("%Y-%-m/%-d")  

        mapping = item.get("mapping", {})
        for value in mapping.values():
            message = value.get("message", {})
            if message:
                message_create_time = message.get("create_time")
                if not message_create_time:
                    continue
                logs_datetime = datetime.fromtimestamp(message_create_time)

                strftime = logs_datetime.strftime("%Y-%m/%d")  
                # 自分の会話だけ取得する意図
                author = message.get("author", {})
                role = author.get("role", "")
                if role == "user":
                    #ログの中身を掘っていく
                    content = message.get("content")
                    if content:
                        parts = content.get("parts", [])
                        # print(parts)
                        # parts_text = "\n".join(parts)
                        parts_text = "\n".join(p for p in parts if isinstance(p, str))

                        conversations[title]["create_time"] = create_time
                        conversations[title]["logs_by_date"][strftime].append({
                            "text": parts_text,
                            "time": message_create_time
                        })
                        # print(conversations)
    # print("件数:", len(conversations))
    # print(conversations.keys())
    # return dict(conversations)
    # 👇ここから変換処理
    # テンプレートに渡す用
    result = {}

    for title, data in conversations.items():

        # 1つのタイトル分の中身を作る用
        sorted_logs_by_date = {}

        for date, logs in sorted(
            data["logs_by_date"].items(),
            key=lambda x: x[0],
            reverse=True
        ):  
            sorted_logs = sorted(
                logs,
                key=lambda x: x["time"],
                reverse=True
            )

            sorted_logs_by_date[date] = sorted_logs

        result[title] = {
            "create_time": data["create_time"],
            # "logs_by_date": dict(data["logs_by_date"])
            "logs_by_date": sorted_logs_by_date
        }

    return result

def sort_conversations(extracted_conversations):
        return dict(
            sorted(
                extracted_conversations.items(),
                key=lambda x: x[1]["create_time"],
                reverse=True
            )
        )


def upload_zip(request):
    """zipファイルをアップロードして、conversations.jsonの内容を解析して表示する"""
    # 最初に開いたとき
    if request.method == "GET" and not request.GET:
        return render(request, "logs/upload_zip.html")
    
    # アップロードされたとき
    if request.method == "POST":
        zip_file = request.FILES.get("zip_file")

        if not zip_file:
            return render(request, "logs/upload_zip.html", {"error": "zipファイルを選択してください"})
        # 呼び出しと返り値の格納を同時に行なっている
        zip_data = extract_json_from_zip(zip_file) 
        # zip → jsonデータ抽出完了

        if not zip_data:
            return render(request, "logs/upload_zip.html", {"error": "conversations.jsonが見つかりませんでした"})

        # json → 表示用のデータに整形完了
        extracted_conversations = parse_conversations(zip_data)

        sorted_data = sort_conversations(extracted_conversations) 
        
        # 結果表示
        return render(request, "logs/import_json.html", {
            "data": sorted_data
        }) 





# Create your views here.
