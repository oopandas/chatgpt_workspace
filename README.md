# ChatGPT Log Search

## Overview(概要)

ChatGPTのエクスポートデータ(conversations.json)を解析し、
タイトル・日付・ユーザー発言を時系列で整理して可視化するwebアプリです。

長い会話をスクロールせずに、目的の発言へすぐアクセスできることを目的としています。

## Features(特徴)

- タイトルごとの一覧表示
- タイトルのアコーディオン表示
- 日付ごとのログ分割
- タイトル・日付・ログをすべて新しい順にソート表示
- 貼り付け用のコピーボタン
- 長いスクロールをせずに目的の会話へアクセス可能
- タイトル・日付の二段階アコーディオンを表示
- 日付ごとのログ件数表示

## Live Demo

### AWS (現在公開中)

https://chatgpt-search.aws-and-infra-study-test.com/

> EC2 + Nginx + Gunicorn + Djangoで公開

### Render版 (初期デプロイ環境)

https://chatgpt-workspace.onrender.com/

> 初めてWebへ公開した環境

## Tech Stack(使用技術)

### Backend
- Python 3.x
- Django 5.x
- Gunicorn

### Frontend 
- Bootstrap

### Web Server
- Nginx

### Infrastructure
- AWS EC2
- Cloudflare

### Previous Deployment
- Render 

### Others
- Python-dotenv

## Architecture(構造設計)

```text
訪問者
  │
  ▼
Cloudflare
(DNS / ドメイン管理)
  │
  ▼
AWS EC2
  │
  ▼
Nginx
  │
  ▼
Gunicorn
  │
  ▼
Django
```
データの流れ: zipファイルからconversations.jsonを抽出 → title/create_time/content.partsを抽出 → 「タイトル→日付→ログ」の構造に整形 → 時系列でソート → Djangoテンプレートで表示

## What I Learned(学んだこと)

- データ構造の設計: 「タイトル→日付→ログ」を表現するため、defaultdictとlistを組み合わせた入れ子構造を設計。ネストされたJSON(mapping配下のmessage/content/parts)をNoneチェックしながら安全に取り出す方法を学んだ
- 時系列ソートの実装: 各ログにcreate_timeを付与し、タイトル・日付・ログの複数階層を新しい順にソート。日付を文字列でゼロ埋めしないと辞書順ソートで崩れる問題にも対処した
- AWSでのインフラ構築: EC2上でNginx(リバースプロキシ)+ Gunicorn + Djangoの構成を一から構築し、CloudflareでDNSを設定。Renderと異なり、Webサーバー層を自分で構築する経験ができた

試行錯誤の詳細(デプロイ時のエラー対応など)は[docs/DEVLOG.md](docs/DEVLOG.md)にまとめています。

## Environment setup procedure(環境設定)

### 1. Clone the repository
```bash
git clone https://github.com/oopandas/chatgpt_workspace.git
cd chatgpt_workspace/django_chatlog_project/chatgpt_talk_search  
```

### 2. Create a virtual environment
```bash
python -m venv venv  
source venv/bin/activate # Mac/Linux  
venv\Scripts\activate    # Windows  
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a .env file
Create a `.env` file in the project root and add:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
```

### 5. Run the development server
```bash
python manage.py runserver
```

## 利用上の注意

- 本アプリはアップロードされたデータを一時的に処理するためのツールです
- アップロードされたファイルはメモリ上で処理しており、ディスクへの書き出しおよびデータベースへの保存は行っていません
- 個人情報や機密情報を含むデータのアップロードは自己責任で行ってください
- 本アプリの利用によって生じた損害について、開発者は責任を負いません

## 今後の改善点

- リアルタイムでログを取得・反映できる仕組みの実装
- UI改善（長文ログの折りたたみ）
- 複数AIサービス（Claude / Gemini）への対応
- S3への画像・JSONファイル保存
- ALBで使用ユーザーが増えた際の負荷分散
