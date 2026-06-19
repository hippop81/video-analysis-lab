# Video Analysis Lab

## Silence Review UI

`silence_detector.py` が出力した `silence.json` を読み込み、無音候補を1件ずつ確認して「採用 / スキップ」を判断するレビューUI。

### セットアップ

```bash
# 1. 依存パッケージをインストール
pip install -r requirements.txt

# 2. UIを起動
streamlit run silence_review_ui.py
```

ブラウザが自動で開きます（デフォルト http://localhost:8501）。

### 使い方

1. 画面上部から `silence.json` をアップロード
2. 各候補を「採用」「スキップ」ボタンで判断（前へ/次へで移動可能）
3. 完了したら「レビュー結果をダウンロード」ボタンでJSONを保存

### エクスポート形式

レビュー結果は解析JSON（silence.json）とは別ファイルとして保存されます。

```json
{
  "type": "silence_review",
  "source_file": "silence.json",
  "candidates": [
    {
      "id": "silence_0001",
      "candidate_type": "silence",
      "start": 12.300,
      "end": 14.100,
      "duration": 1.800,
      "status": "adopted"
    }
  ]
}
```

### サンプルデータ

`sample_silence.json` をテスト用に同梱しています。
