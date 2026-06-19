"""Silence Review UI — Streamlitベースの無音候補レビューツール."""

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

CANDIDATE_TYPE = "silence"


def load_silence_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    silences = data["results"]["silences"]
    candidates = []
    for i, s in enumerate(silences):
        candidates.append(
            {
                "id": f"silence_{i + 1:04d}",
                "candidate_type": CANDIDATE_TYPE,
                "start": s["start"],
                "end": s["end"],
                "duration": s["duration"],
                "status": "pending",
            }
        )
    return candidates


def format_time(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{s:05.2f}"


def build_export(candidates: list[dict], source_file: str) -> dict:
    return {
        "type": "silence_review",
        "source_file": source_file,
        "candidates": [
            {
                "id": c["id"],
                "candidate_type": c["candidate_type"],
                "start": c["start"],
                "end": c["end"],
                "duration": c["duration"],
                "status": c["status"],
            }
            for c in candidates
        ],
    }


def main():
    st.set_page_config(page_title="Silence Review", layout="centered")
    st.title("Silence Review")

    uploaded = st.file_uploader("silence.json をアップロード", type=["json"])
    if uploaded is None:
        st.info("silence.json を読み込んでください。")
        return

    source_name = uploaded.name

    if "candidates" not in st.session_state or st.session_state.get("_source") != source_name:
        raw = json.loads(uploaded.read())
        silences = raw["results"]["silences"]
        candidates = []
        for i, s in enumerate(silences):
            candidates.append(
                {
                    "id": f"silence_{i + 1:04d}",
                    "candidate_type": CANDIDATE_TYPE,
                    "start": s["start"],
                    "end": s["end"],
                    "duration": s["duration"],
                    "status": "pending",
                }
            )
        st.session_state.candidates = candidates
        st.session_state.current_index = 0
        st.session_state._source = source_name

    candidates = st.session_state.candidates
    total = len(candidates)

    if total == 0:
        st.warning("候補が0件です。")
        return

    idx = st.session_state.current_index

    # --- 進捗サマリー ---
    pending_count = sum(1 for c in candidates if c["status"] == "pending")
    adopted_count = sum(1 for c in candidates if c["status"] == "adopted")
    skipped_count = sum(1 for c in candidates if c["status"] == "skipped")

    col_p, col_a, col_s = st.columns(3)
    col_p.metric("未判断", pending_count)
    col_a.metric("採用", adopted_count)
    col_s.metric("スキップ", skipped_count)

    st.divider()

    # --- ナビゲーション ---
    nav_left, nav_center, nav_right = st.columns([1, 2, 1])
    with nav_left:
        if st.button("◀ 前へ", disabled=(idx == 0), use_container_width=True):
            st.session_state.current_index -= 1
            st.rerun()
    with nav_center:
        st.markdown(
            f"<h3 style='text-align:center; margin:0'>{idx + 1} / {total}</h3>",
            unsafe_allow_html=True,
        )
    with nav_right:
        if st.button("次へ ▶", disabled=(idx == total - 1), use_container_width=True):
            st.session_state.current_index += 1
            st.rerun()

    st.divider()

    # --- 候補詳細 ---
    c = candidates[idx]

    detail_cols = st.columns(4)
    detail_cols[0].markdown(f"**ID** `{c['id']}`")
    detail_cols[1].markdown(f"**Start** {format_time(c['start'])}")
    detail_cols[2].markdown(f"**End** {format_time(c['end'])}")
    detail_cols[3].markdown(f"**Duration** {c['duration']:.3f}s")

    status_label = {"pending": "⏳ pending", "adopted": "✅ adopted", "skipped": "⏭️ skipped"}
    st.markdown(f"**ステータス:** {status_label[c['status']]}")

    # --- アクションボタン ---
    btn_cols = st.columns(3)
    with btn_cols[0]:
        if st.button("✅ 採用", use_container_width=True, type="primary"):
            candidates[idx]["status"] = "adopted"
            if idx < total - 1:
                st.session_state.current_index += 1
            st.rerun()
    with btn_cols[1]:
        if st.button("⏭️ スキップ", use_container_width=True):
            candidates[idx]["status"] = "skipped"
            if idx < total - 1:
                st.session_state.current_index += 1
            st.rerun()
    with btn_cols[2]:
        if st.button("↩️ pendingに戻す", use_container_width=True):
            candidates[idx]["status"] = "pending"
            st.rerun()

    st.divider()

    # --- エクスポート ---
    export_data = build_export(candidates, source_name)
    export_json = json.dumps(export_data, indent=2, ensure_ascii=False)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_filename = f"silence_review_{timestamp}.json"

    st.download_button(
        label="📥 レビュー結果をダウンロード",
        data=export_json,
        file_name=export_filename,
        mime="application/json",
        use_container_width=True,
    )

    # --- 一覧テーブル ---
    with st.expander("全候補一覧"):
        table_data = []
        for i, c in enumerate(candidates):
            table_data.append(
                {
                    "#": i + 1,
                    "ID": c["id"],
                    "Start": format_time(c["start"]),
                    "End": format_time(c["end"]),
                    "Duration": f"{c['duration']:.3f}s",
                    "Status": c["status"],
                }
            )
        st.dataframe(table_data, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
