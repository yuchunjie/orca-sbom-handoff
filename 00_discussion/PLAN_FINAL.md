# PLAN_FINAL — 正式執行計畫 (基於 PLAN_V1，納入決策與已知風險)

> **來源**: PLAN_V1 (唯一版本，Agent 1–3 缺席 >30 分鐘)
> **狀態**: 採用「最低分最高」規則 (僅有 V1)，未通過條目列入已知風險
> **生效**: 即時進入 Stage 1–5 實作

---

## 1. 最終流程與各階段負責人 (單人全包)

| 階段 | 名稱 | 負責人 | 輸出目標 |
|------|------|--------|----------|
| 1 | SBOM 生成 | Agent 4 (兼任 Agent 1) | SPDX + CycloneDX + OSV 查詢結果 |
| 2 | VEX 產出 | Agent 4 (兼任 Agent 1) | CycloneDX VEX (每判斷含來源) |
| 3 | Pages 發布 | Agent 4 (兼任 Agent 2) | GitHub Pages 固定 URL + Actions workflow |
| 4 | Apps Script | Agent 4 (兼任 Agent 3) | .gs 代碼 + Sheet demo + Email demo |
| 5 | 影片合成 | Agent 4 | final.mp4 + final.srt + materials_map.csv |

---

## 2. 關鍵技術決策 (單方面決定，風險已知)

| 決策項 | 選擇 | 理由 | 風險緩解 |
|--------|------|------|----------|
| Zephyr 版本 | 3.6.0 (LTS) | 穩定、文檔全、OSV 有歷史漏洞 | 若 OSV 無資料，改用示範選例 |
| Target Board | `qemu_x86` | 雲端 CI 可跑、無硬體依賴、建置快 | 非實體板卡，影片說明 |
| 範例 App | `samples/hello_world` | 最小、無外部依賴、SBOM 乾淨 | 元件少 → VEX 示範用示範選例 |
| SBOM 格式 | SPDX 2.3 → CycloneDX 1.6 | `west spdx` 原生、cyclonedx-python 轉換 | 驗證 PURL 保留 |
| VEX 格式 | CycloneDX VEX 1.0 | Schema 嚴格、工具支援好、可內嵌於 SBOM | 每 vulnerability 必填 state/justification/detail/source_url |
| Pages URL | `/sbom/latest.cdx.json` 等固定路徑 | 可預測、Apps Script 直抓、無版本號 | Actions 部署到 `gh-pages` branch |
| Apps Script | 時間觸發 (每日 02:00) + PropertiesService | 無伺服器、免費、最小權限 | 配額監控、分批處理、錯誤重試 |
| 影片工具鏈 | ffmpeg (libass) + say + whisper.cpp | 全本地、免費、可腳本化、macOS 原生 | 預先重編 ffmpeg、備援 moviepy |

---

## 3. 介面契約 (Contracts) — 單方面定義，實作時同步修正

### 3.1 SBOM/VEX 輸出 (`01_sbom_vex/output/`)
```json
// sbom.cdx.json — CycloneDX 1.6
{ "bomFormat": "CycloneDX", "specVersion": "1.6", "components": [ { "purl": "pkg:generic/zephyr/kernel@3.6.0", ... } ] }

// vex.cdx.json — CycloneDX VEX 1.0
{ "vulnerabilities": [ { "id": "CVE-2024-XXXX", "analysis": { "state": "not_affected", "justification": "code_not_present", "detail": "Kernel config disables vulnerable module. Source: https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xxxx", "response": ["upgrade"] } } ] }

// osv_query_batch.json — OSV 批次查詢原始回應
```

### 3.2 Pages URLs (固定)
- `https://yuchunjie.github.io/orca-sbom-handoff/sbom/latest.cdx.json`
- `https://yuchunjie.github.io/orca-sbom-handoff/sbom/latest.spdx.json`
- `https://yuchunjie.github.io/orca-sbom-handoff/vex/latest.json`
- `https://yuchunjie.github.io/orca-sbom-handoff/` (首頁，可選)

### 3.3 Apps Script 介面
- **輸入**: 上述 3 個 Pages URLs
- **輸出**: Google Sheet (欄位: CVE, Package, Version, OSV_Severity, VEX_Status, VEX_Justification, Checked_At, Quota_Used)
- **觸發**: 每日 02:00 UTC 時間驅動
- **Secrets**: `OSV_API_KEY` (可選), `SHEET_ID`, `RECIPIENT_EMAIL` → `PropertiesService`
- **Scopes**: `spreadsheets`, `script.send_mail`, `urlfetch`

### 3.4 影片素材需求 (`04_video/materials_request.md`)
各階段需提供：關鍵指令截圖/錄影、確切數值 (命中數、判斷數、耗時、配額)、所有 CVE ID/版本/URL

---

## 4. Gate 檢查項 (客觀可驗證)

| Gate | 驗證指令/方式 | 通過標準 |
|------|---------------|----------|
| G1: SPDX/CycloneDX Schema | `cyclonedx validate -i 01_sbom_vex/output/sbom.cdx.json` | Exit code 0 |
| G2: VEX 完整性 | `jq '.vulnerabilities[] | select(.analysis.state==null or .analysis.justification==null or .analysis.detail==null)' 01_sbom_vex/output/vex.cdx.json` | 空輸出 |
| G3: VEX 來源可查證 | `jq -r '.vulnerabilities[].analysis.detail' 01_sbom_vex/output/vex.cdx.json | grep -E '^https?://'` | 每行都是有效 URL |
| G4: Pages URL 可達 | `curl -f -sSL <url> | jq -e .bomFormat` | 全部 Exit 0 |
| G5: Pages 更新生效 | Push 後 30 秒內 `curl` 取得新內容 | 內容含新 commit hash |
| G6: Apps Script 執行 | 手動 `clasp run` 或觸發器 → Sheet 寫入 → Email 收到 | 有新漏洞時寄信、無變更不寄、冪等 |
| G7: 影片旁白核實 | 逐句對照各階段 DONE.md | 0 差異 |
| G8: 影片技術指標 | `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 final.mp4` | 600–900 秒；抽查 5 點音畫同步 <100ms |

---

## 5. 範圍分級 (Must/Should/Could) — 執行時依序砍 Could → Should

| 項目 | 等級 | 實作順序 |
|------|------|----------|
| Zephyr hello_world + qemu_x86 建置 | Must | 1 |
| `west spdx` 產 SPDX | Must | 2 |
| SPDX → CycloneDX (cyclonedx-python) | Must | 3 |
| OSV querybatch 查詢 | Must | 4 |
| CycloneDX VEX 產出 (含示範選例) | Must | 5 |
| GitHub repo + Actions workflow | Must | 6 |
| Pages 部署固定 URL | Must | 7 |
| Apps Script 完整流程 (模擬/真實) | Must | 8 |
| 影片旁白草稿 + 分鏡 | Must | 9 |
| 錄影/TTS/字幕/合成 | Must | 10 |
| 人類可讀 Pages 首頁 | Should | 11 |
| 兩種轉換工具對比 | Should | 12 |
| 影片片頭/片尾 | Could | 13 |

---

## 6. 八大議題最終結論

| 議題 | 結論 | 備註 |
|------|------|------|
| 1. Zephyr 元件 OSV 比對與誠實呈現 | 實測命中率；<30% 改用 3 個示範選例 + 明確標示 | 已知風險 |
| 2. VEX demo 策略 | CycloneDX VEX 1.0；每判斷含 source_url；示範選例標示 | 已定 |
| 3. 範例 app/board/版本 | hello_world / qemu_x86 / Zephyr 3.6.0 | 已定 |
| 4. Pages 首頁 | Could (不阻擋主流程) | 可選 |
| 5. Apps Script secrets/scopes/配額 | PropertiesService + 最小 scopes + 配額記錄欄 | 已定 |
| 6. 影片敘事/工具鏈 | 線性 + CVE 貫穿；ffmpeg+say+whisper.cpp | 已 spike 驗證 |
| 7. Repo 結構 | `orca-sbom-handoff/` 為 demo repo | 已定 |
| 8. 範圍取捨 | 見 §5 表格 | 已定 |

---

## 7. 已知風險與降級預案 (源自 Agent 1–3 缺席)

| 風險 | 影響 | 降級預案 | 標註位置 |
|------|------|----------|----------|
| OSV 命中率極低/為零 | VEX 內容空、敘事無力 | 使用 3 個真實 Zephyr 歷史 CVE 做示範選例，旁白/字幕雙重標示 | DONE.md、影片字幕、旁白 |
| west spdx 不支援 Zephyr 3.6 | 無法產 SPDX | 改用 `syft` 或 `trivy` 掃描建置產物 | DONE.md、影片口頭說明 |
| Actions 建置超時/失敗 | Pages 無內容 | 本機 `python3 -m http.server` 模擬 Pages，標註「本機模擬」 | DONE.md、影片字幕 |
| Apps Script 配額/時間不足 | 無法完整跑完 | 本機 Node 模擬邏輯驗證，影片展示代碼而非實際執行 | DONE.md、影片字幕 |
| ffmpeg libass 重編失敗 | 無法燒字幕 | 用 moviepy (Python) 燒字幕，或硬字幕預渲染 | DONE.md、技術選型記錄 |

---

## 8. Preflight 缺項與降級 (已確認)

| 項目 | 狀態 | 降級方案 |
|------|------|----------|
| P1: gh auth | ✅ 通過 | N/A |
| P2: clasp | ❌ 未安裝 | Apps Script 代碼完整、本機 Node 模擬驗證邏輯，標註「未真實部署」 |
| P3: ffmpeg/west/python/node | ⚠️ west 已補裝 | ffmpeg 需重編 libass (預留 15 分鐘) |

---

## 9. [UNVERIFIED] 清單 (實作前必須驗證)

- [ ] `west spdx` 在 Zephyr 3.6.0 + qemu_x86 實際輸出格式
- [ ] SPDX → CycloneDX 轉換 PURL 保留完整度
- [ ] OSV querybatch 對 hello_world SBOM 實際命中數
- [ ] GitHub Actions 建置 Zephyr 耗時 (含快取)
- [ ] Apps Script 解析 CycloneDX + OSV 查詢 實際耗時/配額
- [ ] ffmpeg 重編 libass 成功率
- [ ] whisper.cpp 對繁體中文旁白辨識準確度

---

## 10. 實作啟動順序

1. **Stage 1+2** (SBOM/VEX): `01_sbom_vex/` — 建置 Zephyr、產 SPDX、轉 CycloneDX、查 OSV、產 VEX
2. **Stage 3** (Pages): `02_pages_ci/` — 建立 repo、寫 Actions、部署 Pages、驗證 URL
3. **Stage 4** (Apps Script): `03_apps_script/` — 寫 .gs、部署/模擬、產出 Sheet/Email 截圖
4. **Stage 5** (Video): `04_video/` — 寫旁白、分鏡、錄影/TTS、whisper 字幕、ffmpeg 合成、核對
5. **Final**: `FINAL_REPORT.md` 彙整

---

**下一步**: 進入 Stage 1+2 — SBOM 與 VEX 產出。先建立 Zephyr workspace 並驗證 `west spdx`。