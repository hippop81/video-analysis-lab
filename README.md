# Video Analysis Lab

Video/audio analysis experiments for finding review candidates before editing. The current repository contains a Streamlit UI for reviewing silent sections detected by a separate `silence_detector.py` output.

## Current Features

### Silence Review UI

`silence_detector.py` が出力した `silence.json` を読み込み、無音候補を1件ずつ確認して「採用 / スキップ」を判断するレビューUIです。

このUIは動画や音声ファイルを直接編集しません。解析済みJSONを読み込み、レビュー結果JSONを出力するだけです。

## Current File Structure

```text
.
├── README.md
├── requirements.txt
├── silence_review_ui.py
├── sample_silence.json
└── docs/
    ├── analysis-pipeline-notes.md
    └── project-structure.md
```

現時点で実装済みのPythonアプリは `silence_review_ui.py` です。`docs/analysis-pipeline-notes.md` にある detector / summary scripts は、今後追加予定の解析パイプラインメモです。

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

```bash
streamlit run silence_review_ui.py
```

ブラウザが自動で開きます（デフォルト http://localhost:8501）。

## Review Flow

1. 画面上部から `silence.json` をアップロード
2. 各候補を「採用」「スキップ」ボタンで判断（前へ/次へで移動可能）
3. 完了したら「レビュー結果をダウンロード」ボタンでJSONを保存

## Input Format

`silence_review_ui.py` は次のような `results.silences` 形式を読み込みます。

```json
{
  "results": {
    "silences": [
      {"start": 12.300, "end": 14.100, "duration": 1.800}
    ]
  }
}
```

`sample_silence.json` をテスト用に同梱しています。

## Export Format

レビュー結果は解析JSON（`silence.json`）とは別ファイルとして保存されます。

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

## Expansion Notes

今後のフォルダ整理案は `docs/project-structure.md` にまとめています。今回のcleanupでは既存スクリプトの動作を変えないため、`silence_review_ui.py` の移動やimport path変更は行っていません。
