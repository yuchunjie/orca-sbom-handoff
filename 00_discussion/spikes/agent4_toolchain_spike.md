# Agent 4 Spike: Video Toolchain Verification

## Test Date: 2026-10-23

## Pipeline Steps Tested

| Step | Tool | Status | Evidence |
|------|------|--------|----------|
| Screen recording | `ffmpeg -f avfoundation -i "4:none"` | ✅ PASS | `screen_raw.mp4` (4.23s, 3420×2214, 1346 KiB) |
| TTS generation | `say -v Ting-Ting` | ✅ PASS | `narration.aiff` → `narration.wav` (3.47s, 16kHz mono) |
| Audio/Video compose | `ffmpeg -i video -i audio -shortest` | ✅ PASS | `combined.mp4` (3.47s, 3420×2214, 1270 kbps) |
| Auto-subtitle (ASR) | Whisper.cpp `base` model | ✅ PASS | `subtitles.srt` generated in 790ms |
| Subtitle burning | `ffmpeg -vf subtitles=` | ❌ FAIL | **libass not compiled in Homebrew ffmpeg** |
| Fallback: drawtext | `ffmpeg -vf drawtext=` | ❌ FAIL | **libfreetype not compiled** |

## Whisper.cpp Output (subtitles.srt)
```
1
00:00:00,000 --> 00:00:03,320
 这是测试庞白,展示工具链运作
```
- Language: Simplified Chinese (whisper base model default)
- Timing: Accurate to TTS duration (3.32s vs 3.47s source)
- Note: For production, use `whisper.cpp` with `--language zh` and Traditional Chinese prompt, or fine-tuned model.

## Workaround for Subtitle Burning

**Option A (Recommended)**: Rebuild ffmpeg with `--enable-libass --enable-libfreetype`
```bash
brew uninstall ffmpeg && brew install ffmpeg --with-libass --with-freetype
# Or compile from source
```

**Option B**: Python + moviepy (scriptable, has text rendering)
```python
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
# Render subtitles frame-by-frame
```

**Option C**: Two-pass - generate subtitle images with ImageMagick/PIL, overlay with ffmpeg `overlay` filter (no libass needed).

**Option D**: Use `whisper.cpp` JSON output → generate ASS file → use `ffmpeg -vf ass=sub.ass` (still needs libass).

## Decision for Production

**Use Option A**: Rebuild ffmpeg with libass/freetype. It's the cleanest, keeps everything in ffmpeg, and ASS format supports styling/positioning better than SRT.

Time estimate: 10–15 min to recompile ffmpeg on macOS (Apple Silicon).

## Spike Summary
- **Core pipeline (record → TTS → compose → ASR) works end-to-end** ✅
- **Only missing piece**: subtitle burn-in requires ffmpeg rebuild
- **Total spike time**: ~25 minutes (including whisper.cpp build + model download)
- **Verdict**: Toolchain is viable. Proceed with ffmpeg rebuild before Stage 5.

## Files Generated
```
/Users/jie/Desktop/OpenCode_Proj/orca-sbom-handoff/04_video/spike_assets/
├── screen_raw.mp4      # Raw screen capture
├── narration.aiff      # macOS say output
├── narration.wav       # 16kHz mono for whisper
├── combined.mp4        # Video + audio composed
├── subtitles.srt       # Whisper.cpp output
└── final_drawtext.mp4  # (failed)
```