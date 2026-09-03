from django.shortcuts import render
import json, zipfile
from datetime import datetime
from collections import defaultdict


def extract_json_from_zip(zip_file):
    """zipからjsonを抽出"""

    conversations_data = []

    with zipfile.ZipFile(zip_file) as zip_ref:
        # ディスクに展開せず、直接ファイル名一覧を取得
        for file in zip_ref.namelist():
            # conversations.json(複数分割されている可能性がある)を検出
            if file.startswith("conversations") and file.endswith(".json"):
                    # 必要なファイルのみメモリ上で直接読み込む
                    with zip_ref.open(file) as f:
                        data = json.load(f)
                        conversations_data.extend(data)
                        
    return conversations_data

def parse_conversations(zip_data):
    """conversations.jsonの内容を解析して、会話のタイトルと日付ごとに会話の内容に整形"""
    
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

        mapping = item.get("mapping", {})
        # conversations.jsonはツリー構造のため、各メッセージを掘っていく
        for value in mapping.values():
            message = value.get("message", {})
            if message:
                message_create_time = message.get("create_time")
                if not message_create_time:
                    continue
                logs_datetime = datetime.fromtimestamp(message_create_time)

                # 日付単位でグループ化するため文字列に変換
                strftime = logs_datetime.strftime("%Y-%m/%d")  
                # 自分の会話だけ取得する意図
                author = message.get("author", {})
                role = author.get("role", "")
                if role == "user":
                    # messageの中のcontentからユーザーの会話テキストを抽出
                    content = message.get("content")
                    if content:
                        parts = content.get("parts", [])
                        
                        # partsはリストで、テキスト以外の要素も含まれているためテキストだけを抽出して結合する
                        parts_text = "\n".join(p for p in parts if isinstance(p, str))

                        conversations[title]["create_time"] = create_time
                        conversations[title]["logs_by_date"][strftime].append({
                            "text": parts_text,
                            "time": message_create_time
                        })
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
        zip_data = extract_json_from_zip(zip_file) 
        # zip → jsonデータ抽出完了

        if not zip_data:
            return render(request, "logs/upload_zip.html", {"error": "conversations.jsonが見つかりませんでした"})

        # json → 表示用のデータに整形完了
        extracted_conversations = parse_conversations(zip_data)

        sorted_data = sort_conversations(extracted_conversations) 

        # 結果表示
        return render(request, "logs/import_json.html", {
            "data": sorted_data,
        }) 

# Create your views here.
