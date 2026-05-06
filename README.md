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

## Tech Stack(使用技術)

- Python 3.x
- Django 5.x
- Bootstrap
- Python-dotenv
- Render (Deployment)

## Live Demo

https://chatgpt-workspace.onrender.com/

## Architecture(構造設計)
※ データの取得 → 構造化 → ソート → 表示までを一貫して設計
1. 送信されたzipファイルから、conversations.jsonを抽出
2. conversations.jsonからtitle, create_time, message.create_time, content.partsを抽出
3. defaultdictを用いて「タイトル → 日付 → ログ」の構造に整形
4. 各ログにtimeを付与し、ログを時系列でソート
5. 日付ごとにログをまとめ、日付を新しい順にソート
6. タイトルをcreate_timeベースで新しい順にソート
7. Djangoテンプレートに渡して表示
8. Bootstrapでデザイン(アコーディオン)を適用
9. ログの内容にコピーボタンを設置
10. コピーしたテキストをChatGPT内で検索し、該当の会話へ素早く戻れるようにする


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
Create a .env file in the project root and add:

DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

### 5. Run the development server
```bash
python manage.py runserver
```

## What I Learned(学んだこと)

### データ構造の設計
- 「タイトル → 日付 → ログ」の表示にするために、dictとlistを組み合わせた入れ子構造を設計
- 階層構造を一つずつ構築し、表示要件に合わせてデータ構造を設計する重要性を理解

### defaultdictの活用
- defaultdictを用いることで、キーの存在チェックを省略しながらデータを構築できるようになり、条件分岐を減らしたシンプルな構造ができた。

### ネストされたJSONの扱い
- conversations.json(title / mapping / message / content)が深い入れ子
  構造になっており、必要なデータにたどり着くために複数階層を制御構文で辿る必要があった。
- mapping配下の「message→author, content, parts」を取得する際に、
  Noneチェックやgetメソッドの使い方に苦戦した。

- 「どの階層に何のデータがあるか」を整理しながら処理を書くことで、
  安全に入れ子構造のデータを取り出せるようになった。

### 時系列ソートの設計
- 各ログにcreate_timeを持たせることで、
「タイトル・日付・ログ」の全てを時系列でソートできるデータ構造に改善した。

- 初期実装ではタイトルのみをcreate_timeをソートしていたため、
  日付やログの順序が意図した並びにならない問題が発生した。

- ログに時間情報を持たせていなかったため、
  同じ日付内のログの順番もバラバラになっていた。

- 各ログにmessage単位のcreate_timeを付与し、
  日付単位・ログ単位の両方でソートできるデータ構造に改善した。

- 日付を文字列(%Y-%-m/%-d)で扱っていたため、
  辞書順でソートされてしまい、意図しない順序になる問題が発生した。

- ゼロ埋め形式(%Y-%m/%d)に変更することで、
  正しい時系列順で表示できるように修正した。

- sorted関数とlambdaを組み合わせることで、「タイトル・日付・ログ」の複数階層の新しい順のソートを実装することができた。

- sortedの結果がlistになる仕様に対して、テンプレートで扱いやすいように再度dictにする必要があることを理解した。テンプレートで扱いやすくするためのview側の重要性を学ぶことができた。

- 「defaultdictデータを構築、sortedで並び替え、dictに変換してテンプレートに渡す」一連のデータ構造の作成・整形を経験し、データ構造の基本的な流れを理解することができた。

### デプロイ時のエラー（pkg_resources）
- pkg_resources に関するエラー（ModuleNotFoundError）が発生

- 原因は setuptools が正しく読み込まれていないこと

- Build Command内で明示的に setuptools をインストールすることで解決

### Build Commandの実行エラー

- 改行ができないので、一行でコマンドがつながってしまい、正しく実行されなかった
- && を使ってコマンドを連結することで解決

### プロジェクト構成の問題
- requirements.txtが深い階層にあり、正しく読み込まれなかった
- Root Directoryで階層を設定することで解決

### ルーティングの問題
- ルートURL（/）にアクセスすると404エラーが発生
- リダイレクトを追加して、メインページへ遷移するように修正

### デプロイの学び
- ローカルと本番環境の違い（依存関係・実行ディレクトリ）によってエラーが発生することを経験
- エラーの原因をログから特定し、順序や環境設定を調整することで解決できた

## 🔍 今後の改善点

- リアルタイムでログを取得・反映できる仕組みの実装
- UI改善（長文ログの折りたたみ）
- 複数AIサービス（Claude / Gemini）への対応