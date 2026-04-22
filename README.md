# Chatgpt Log Search

## Overview

ChatGptのエクスポートデータ(conversations.json)を解析し、
タイトル・日付・ユーザー発言を時系列で整理して可視化するwebアプリ

## Features

- タイトルの一覧表示
- タイトルのアコーディオン表示
- 日付順にログの内容が分割
- タイトル・日付・ログをすべて時系列(新しい順)でソート表示
- 貼り付け用のコピーボタン

## Tech Stack

- Python 3.x
- Django==5.1
- Bootstrap
- Python-dotenv
## Live Demo

https:

## Architecture
1. 送信されたzipファイルから、conversations.jsonを抽出
2. conversations.jsonからtitle, create_time, message.create_time, content.partsを抽出
3. defaultdictを用いて「タイトル → 日付 → ログ」の構造に整形
4. 各ログにtimeを付与し、ログを時系列でソート
5. 日付ごとにログをまとめ、日付を新しい順にソート
6. タイトルをcreate_timeベースで新しい順にソート
7. Djangoテンプレートに渡して表示
8. Bootstrapでデザイン(アコーディオン)を適用
9. ログの内容にコピーボタンを設置
10. コピーしたテキストをchatgpt内の同じタイトルの会話ないで検索(cmd+f)で貼り付けて戻りたい日付まで遡る

## Environment setup procedure

### 1. Clone the repository
git clone https://github.com/your-username/アプリ名.git  
cd chatgpt_work_space/django_chatlog_project/chatgpt_talk_search  

### 2. Create a virtual environment
python -m venv venv  
source venv/bin/activate # Mac/Linux  
venv\Scripts\activate    # Windows  

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create a .env file
Create a .env file in the project root and add:

DJANGO_SECRET_KEY=your-secret-key
DEBUG=

### 5. Run the development server
python manage.py runserver

## What I Learned


