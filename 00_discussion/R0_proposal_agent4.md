# R0 Proposal — Agent 4 (Video Script & Synthesis, Stage 0 Integrator)

## (a) Overall Video & Flow Design

### Core Narrative: "From Code to Confidence"
A single vulnerability report (CVE-2024-XXXX) threads through the entire 12-minute video:
1. **Hook (0:00–0:45)**: Real advisory screenshot → "This CVE exists in a dependency you ship. Do you know?"
2. **SBOM Chapter (0:45–3:30)**: What is SBOM, why CycloneDX, live `west spdx` → conversion → verify on OSV
3. **VEX Chapter (3:30–6:00)**: Not all CVEs affect you. VEX = "I checked, here's why it's not exploitable." Live VEX generation.
4. **Pages Chapter (6:00–8:00)**: Publish to immutable URLs. CI/CD automates it. `curl` proves it works.
5. **Apps Script Chapter (8:00–10:30)**: Scheduled check → OSV batch query → cross-ref VEX → Sheet + Email. Live demo of email arriving.
6. **Limitations & Next Steps (10:30–11:30)**: Honest about quotas, no UI, when to graduate to Dependency-Track.
7. **Wrap-up (11:30–12:00)**: Repo link, reproducibility commands, call to action.

**Why this structure**: Linear but event-driven. The CVE thread gives viewers a mental anchor. Each chapter answers "so what?" for the previous.

### Toolchain (macOS, Free, Scriptable)
| Task | Tool | Why |
|------|------|-----|
| Screen recording | `ffmpeg -f avfoundation` | Native, no GUI, scriptable |
| TTS (Mandarin) | `say` (macOS built-in) + `ffmpeg` | Zero cost, local, adjustable rate/voice |
| Subtitles | Whisper.cpp (local) → SRT | Offline, accurate, timestamps align |
| Editing/Composition | `ffmpeg` filter_complex | Single binary, frame-accurate, scriptable |
| Slides/Titles | HTML → `puppeteer` → PNG → ffmpeg | Programmable, version-controlled |
| Audio mix | `ffmpeg -filter_complex amix` | Ducking, normalization in one pass |

**Spike will verify**: 10-second end-to-end pipeline (record → TTS → subtitle → composite → MP4 + SRT).

### Deliverables (Agent 4)
- `04_video/script.md` — full narration (Traditional Chinese, technical terms in English)
- `04_video/storyboard.csv` — scene, duration, visual cue, audio source
- `04_video/synthesize.sh` — single script producing `final.mp4` + `final.srt`
- `04_video/assets/` — slides, screenshots, recordings
- `04_video/materials_map.csv` — timestamp ↔ source file ↔ agent ↔ verification status

## (b) Top 3 Risks
1. **Toolchain fragility**: `avfoundation` capture permissions on macOS, TTS voice consistency, Whisper.cpp model download. Mitigation: fallback to pre-recorded clips + `say` only.
2. **Sync drift**: Screen recording frame rate vs TTS duration vs subtitle timing. Mitigation: generate TTS first, measure duration, record to match, then force-align with Whisper.
3. **Upstream data mismatch**: Agent 1/2/3 outputs change after script locked. Mitigation: contract-first (Agent 4 defines placeholders in script; Agents 1–3 fill exact values).

## (c) Interface Contracts Needed
| From | To Agent 4 | Format | Deadline |
|------|------------|--------|----------|
| Agent 1 | SBOM/VEX file paths, exact CVE IDs used, OSV query/response samples | JSON + markdown | Stage 1 DONE |
| Agent 2 | GitHub Pages URLs (stable), Actions run URL, `curl` verification commands | Markdown | Stage 3 DONE |
| Agent 3 | Apps Script code, Sheet URL (or mock), sample email screenshot, quota numbers | .gs + screenshots | Stage 4 DONE |
| All | `DONE.md` with Gate evidence | Markdown | Each stage |

## (d) If Time Halved (6–7 min)
**Cut**: Apps Script deep dive (keep 30s overview + link to code). VEX rationale condensed to 60s. Drop "Limitations" chapter (put in description). Keep: Hook, SBOM generation, VEX generation, Pages publish, one-liner wrap-up.

---

## Spike: Video Toolchain Verification (10-second demo)

**Goal**: Record screen → generate TTS → auto-subtitle → composite → MP4 + SRT. All scriptable, macOS.

**Steps**:
1. Record 5s terminal: `echo "hello"`
2. TTS: `say -v Ting-Ting "這是測試" -o test.aiff`
3. Convert aiff → wav, measure duration
4. Composite: video + audio → MP4
5. Whisper.cpp on audio → SRT
6. Burn subtitles → final.mp4
7. Verify: `ffprobe` duration, SRT timestamps align