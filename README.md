# Chatgpt Log Search

## Overview

このアプリはエクスポートされたデータを使用して、ChatGPT内のログを一覧で表示するアプリです。  
ユーザーは自分のエクスポートしたデータをサイト内にファイルを貼り付けます。  
ファイルのデータの解析が開始されます。    
解析されたデータから、日付、ログのタイトル、質問したテキストの冒頭15行が表示されます。  
冒頭15行をChatGPT内の閲覧したいログの検索欄(cmd+f)で貼り付けることで、特定の日付、遡りたい自分の会話までマウスでスクロールせずに戻ることができます。  

## Features

- 一覧表示(日付/ タイトル/ 質問の冒頭15行)
- 貼り付け用のコピーボタン
- 

## Tech Stack

- Python 3.x
- Django==5.1
- Python-dotenv
## Live Demo

https:

## Environment setup procedure

### 1. Clone the repository
git clone https://github.com/your-username/アプリ名.git  
cd アプリ名  

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


