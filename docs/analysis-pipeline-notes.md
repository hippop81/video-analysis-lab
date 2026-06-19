# Analysis Pipeline Notes

This memo captures the planned small Python scripts for the video/audio analysis workflow. The scripts only detect or summarize analysis data; they do not edit media files.

## Scripts

### beat_detector.py

Purpose: Detect beat timestamps from BGM files such as MP3 or WAV.

- Main library: Librosa
- CLI example: `python3 beat_detector.py --input bgm.mp3 --output beat.json`
- Output fields: `input_file`, `duration`, `tool`, `version`, `results.bpm`, `results.beat_times`
- Number formatting: seconds and BPM should be displayed to three decimal places
- Overwrite behavior: ask before overwriting, or allow overwrite with `--force`

### silence_detector.py

Purpose: Detect silent sections in an MP4 video.

- Main tool: FFmpeg `silencedetect`
- CLI example: `python3 silence_detector.py --input video.mp4 --output silence.json`
- Useful options: `--noise`, `--min-duration`, `--force`
- Output fields: `input_file`, `duration`, `tool`, `version`, `results.silences[]`
- Each silence item: `start`, `end`, `duration`

### scene_detector.py

Purpose: Detect scene changes in an MP4 video.

- Main library: PySceneDetect
- CLI example: `python3 scene_detector.py --input video.mp4 --output scenes.json`
- Useful options: `--threshold`, `--min-scene-len`, `--force`
- Output fields: `input_file`, `duration`, `tool`, `version`, `results.scenes[]`
- Each scene item: `start`, `end`, `duration`

### analysis_summary.py

Purpose: Read the three JSON files above and print a text summary plus warnings.

- Uses only the Python standard library
- Uses `statistics` for averages and beat interval standard deviation
- CLI example: `python3 analysis_summary.py --beat beat.json --silence silence.json --scene scenes.json`
- Useful options: `--near-threshold 0.5`, `--min-scene-len 1.0`
- Supports both JSON shapes:
  - `{ "results": { ... } }`
  - `{ ... }` directly at the top level

## Warning Rules

Only these cases should produce warnings:

- `silence.start` is within `--near-threshold` seconds of `scene.start`
- `silence.end` is within `--near-threshold` seconds of `scene.start`
- A scene start/end timestamp is within `--near-threshold` seconds of another scene start/end timestamp

No other overlap or proximity cases should warn.

## Output Style

The summary script should print sections like:

```text
=== Input Summary ===
beat    | beat_detector    | bgm.mp3   | 180.000 sec
silence | silence_detector | video.mp4 | 600.000 sec
scene   | scene_detector   | video.mp4 | 600.000 sec

=== Silence Summary ===
count: 42
avg: 1.240 sec
min: 0.520 sec
max: 4.810 sec
short_under_1s: 8

=== Beat Summary ===
bpm: 120.000
beat_count: 360
interval_std: 0.012

=== Warnings ===
[WARN] silence start 12.300 is near scene start 12.550
```

At the end, print one short parameter tuning suggestion, for example adjusting the silence threshold, scene minimum length, beat settings, or near-threshold value based on the summary.
