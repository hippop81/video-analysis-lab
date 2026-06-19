# Project Structure Proposal

This document records the cleanup direction for `video-analysis-lab` without changing existing script behavior.

## Current Structure

```text
.
├── README.md
├── requirements.txt
├── silence_review_ui.py
├── sample_silence.json
└── docs/
    └── analysis-pipeline-notes.md
```

Current roles:

- `silence_review_ui.py`: Streamlit app for reviewing silence candidates.
- `sample_silence.json`: Small sample input for the review UI.
- `requirements.txt`: Runtime dependency list for the current UI.
- `docs/analysis-pipeline-notes.md`: Planning memo for detector and summary scripts.

## Proposed Future Structure

When the detector scripts are added, organize files by role:

```text
.
├── README.md
├── requirements.txt
├── apps/
│   └── silence_review_ui.py
├── scripts/
│   ├── beat_detector.py
│   ├── silence_detector.py
│   ├── scene_detector.py
│   └── analysis_summary.py
├── samples/
│   └── sample_silence.json
└── docs/
    ├── analysis-pipeline-notes.md
    └── project-structure.md
```

Suggested roles:

- `apps/`: interactive UI entrypoints such as Streamlit apps.
- `scripts/`: CLI analysis tools that read or produce JSON.
- `samples/`: small test/demo JSON inputs.
- `docs/`: design notes, workflow notes, and project structure guidance.

## Why This PR Does Not Move Files Yet

Moving `silence_review_ui.py` from the repository root to `apps/` would change the current launch command from:

```bash
streamlit run silence_review_ui.py
```

to:

```bash
streamlit run apps/silence_review_ui.py
```

That is a user-facing behavior change, so this cleanup keeps the existing script path intact. No import path changes are required in the current code because `silence_review_ui.py` does not import local project modules.

## Migration Plan

1. Keep the current root-level UI path until detector scripts are added.
2. Add new detector scripts under `scripts/` when implementation starts.
3. Move sample JSON files into `samples/` only when README and UI examples are updated in the same PR.
4. Move Streamlit apps into `apps/` in a dedicated PR, with README command updates and a compatibility note.
5. If shared parsing or formatting logic emerges, introduce a small package such as `video_analysis_lab/` and update imports in a separate tested change.
