# ITrend-Data-collection

Hacker News、はてなブックマーク、Qiita から技術記事を収集し、Gemini で選定・要約して HTML レポートを生成するツールです。

## 特徴

- 3つのソースから記事を取得
- ソースごとのデータを共通フォーマットに正規化
- Gemini でソースごとに記事を選定・要約
- タブ形式の HTML レポートを生成し、ブラウザで表示

## 動作要件

- Python 3.10+
- Gemini API キー

## セットアップ

1. 依存ライブラリをインストール

```bash
pip install requests feedparser python-dotenv google-genai
```

2. `.env_example` から `.env` を作成

```bash
copy .env_example .env
```

3. `.env` に API キーを設定

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash
```

## 実行方法

```bash
python -m src.main
```

実行すると `src/output/result.html` が生成され、既定ブラウザで自動表示されます。

## ディレクトリ構成

```text
src/
  main.py                     # エントリーポイント
  config.py                   # 環境変数の読み込み
  fetchers/
    hackernews.py             # Hacker News (Algolia API)
    hatena.py                 # はてなブックマーク RSS
    qiita.py                  # Qiita API
  services/
    gemini_service.py         # Gemini による選定・要約
```

## 注意事項

- `GEMINI_API_KEY` が未設定の場合、起動時にエラーになります。
- `src/output/` は `.gitignore` で除外されています。
