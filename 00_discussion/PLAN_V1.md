# PLAN_V1 — 初版整合計畫 (Agent 4 整合)

> **備註**：Agent 1–3 的 R0 提案與 spike 尚未出現（已等待 >30 分鐘）。本版僅依 Agent 4 提案與自身 spike 編製，缺口標註 `[MISSING]`。後續版本將納入他們輸入。

---

## 1. 與前版比較（首版，無前版）

## 2. 最終流程與各階段負責人

| 階段 | 名稱 | 負責人 | 輸入 | 輸出 | Gate |
|------|------|--------|------|------|------|
| 0 | 評分迴圈 | Agent 4 (彙整) | 全員 R0 + spike | PLAN_FINAL.md | 4×10/10 |
| 1 | SBOM 生成 | Agent 1 | Zephyr repo, west | SPDX + CycloneDX + VEX | Schema 驗證、CVE 可查證 |
| 2 | VEX 產出 | Agent 1 | SBOM, OSV 查詢結果 | VEX (CycloneDX/OpenVEX) | 每判斷有來源連結 |
| 3 | Pages 發布 | Agent 2 | SBOM/VEX 檔 | GitHub Pages URLs, Actions workflow | `curl` 可取得、重新 push 更新 |
| 4 | Apps Script | Agent 3 | Pages URLs, VEX | .gs 代碼, Sheet, Email demo | 執行成功、冪等、錯誤處理 |
| 5 | 影片合成 | Agent 4 | 全階段 DONE.md | final.mp4 + final.srt + materials_map.csv | 旁白核實、時長、同步抽查 5 點 |

## 3. 介面契約 (Interface Contracts)

### 3.1 Agent 1 → Agent 2/4 (SBOM/VEX)
- **路徑**: `01_sbom_vex/output/`
- **檔案**:
  - `sbom.spdx.json` — SPDX 2.3, 已驗證
  - `sbom.cdx.json` — CycloneDX 1.6, PURL 保留完整
  - `vex.cdx.json` — CycloneDX VEX 1.0 (或 OpenVEX)，每 vulnerability 有 `analysis.state` + `analysis.justification` + `analysis.detail` (含來源 URL)
  - `osv_query_batch.json` — OSV querybatch 原始回應（供 Agent 3/4 核對）
  - `cve_sources.md` — 每 CVE 的查證連結 (OSV/NVD/Zephyr advisory)
- **Schema 驗證**: `cyclonedx-python` / `spdx-tools` / `vex-validator`

### 3.2 Agent 2 → Agent 3/4 (Pages URLs)
- **公開 URL 規則** (固定、可預測):
  - `https://<org>.github.io/<repo>/sbom/latest.cdx.json`
  - `https://<org>.github.io/<repo>/sbom/latest.spdx.json`
  - `https://<org>.github.io/<repo>/vex/latest.json`
  - `https://<org>.github.io/<repo>/` — 首頁 (可選，人類可讀摘要)
- **Actions 產物**: `workflow_dispatch` + `push` 觸發，上傳到 `gh-pages` branch
- **驗證指令**: `curl -sSL <url> | jq .bomFormat` 等

### 3.3 Agent 3 → Agent 4 (Apps Script 成品)
- **檔案**: `03_apps_script/main.gs`, `03_apps_script/config.gs`
- **Secrets 管理**: `PropertiesService.getScriptProperties()` 存 `OSV_API_KEY` (可選), `SHEET_ID`, `RECIPIENT_EMAIL`
- **Scopes**: `https://www.googleapis.com/auth/spreadsheets`, `https://www.googleapis.com/auth/script.send_mail`, `https://www.googleapis.com/auth/urlfetch`
- **觸發器**: 時間驅動 (每日 02:00 UTC)
- **輸出**: Sheet 每列 = 一漏洞 (CVE, Package, Version, OSV Severity, VEX Status, VEX Justification, Checked At)
- **郵件**: 有新漏洞/狀態變更時寄送，無變更不寄
- **配額記錄**: `UrlFetchApp.getUrlFetchQuotaUsed()` 寫入 Sheet 末欄

### 3.4 Agent 4 → 全員 (影片素材需求)
- **需求清單** (`04_video/materials_request.md`):
  - 每階段關鍵指令截圖/錄影 (Agent 1: `west spdx` 輸出; Agent 2: Actions run 頁面; Agent 3: Sheet + Email)
  - 確切數值: OSV 命中數、VEX 判斷數、配額消耗、Actions 耗時
  - 所有 CVE ID、版本號、URL

---

## 4. 各階段 Gate 檢查項

| Gate | 驗證方式 | 失敗處理 |
|------|----------|----------|
| G1: SPDX/CycloneDX Schema | `cyclonedx validate -i sbom.cdx.json` | 修正輸出重試 ≤3 次 |
| G2: VEX 完整性 | 每 vulnerability 有 state+justification+detail+source_url | 補齊後重試 |
| G3: Pages URL 可達 | `curl -f -sSL <url> | jq -e .` | 檢查 Actions log、權限、branch |
| G4: Apps Script 執行 | 手動執行 → Sheet 寫入 → Email 收到 | 除錯 log、調整配額/錯誤處理 |
| G5: 影片旁白核實 | 逐句對照 DONE.md 數值、連結 | 修正旁白/字幕重渲 |
| G6: 影片技術指標 | `ffprobe` 時長 ±2min, 抽查 5 點同步 | 重新合成 |

---

## 5. 範圍分級 (Must/Should/Could)

| 項目 | 等級 | 說明 |
|------|------|------|
| Zephyr 範例 app 建置、SBOM 生成 | Must | 核心示範 |
| CycloneDX 轉換 (至少 1 工具驗證) | Must | 影片需展示 |
| OSV 查詢 + VEX 產出 | Must | 核心價值 |
| GitHub Pages 固定 URL 發布 | Must | 供 Agent 3 使用 |
| GitHub Actions 自動化 | Must | 可重現關鍵 |
| Apps Script 完整流程 (查詢→VEX對照→Sheet→Email) | Must | 核心示範 |
| Apps Script 配額/限制誠實說明 | Must | 可信度關鍵 |
| 影片旁白繁中、專有名詞保留英文 | Must | 觀眾群定義 |
| 影片 10–15 分鐘 | Must | 承諾規格 |
| 人類可讀 Pages 首頁 | Should | 加分項，非必要 |
| 兩種 CycloneDX 轉換工具對比 | Should | Agent 1 spike 已做 |
| OpenVEX 格式支援 | Could | CycloneDX VEX 為主 |
| 影片片頭/片尾動畫 | Could | 時間允許才做 |
| 多語言字幕 | Could | 超出範圍 |

---

## 6. 風險與對策

| 風險 | 影響 | 對策 | 備案 (砍範圍) |
|------|------|------|---------------|
| OSV 對 Zephyr 套件命中率低 | VEX 內容空、敘事無力 | Spike 階段先測命中率；低則改用「示範選例」並明確標示 | 砍 VEX 深度，只示範格式 |
| ffmpeg 缺 libass 無法燒字幕 | Stage 5 卡關 | 預先重編 ffmpeg；或改用 Python moviepy | 字幕改為「燒錄在畫面下方的靜態文字帶」 |
| Apps Script 配額/執行時間不足 | 無法完整跑完 | Spike 測配額；分批處理、續跑機制 | 只示範單次查詢邏輯，不做完整排程 |
| 上游資料變動導致影片對不上 | 影片失真 | 契約先行：Agent 4 定 placeholder，上游填確切值 | 錄影階段鎖定版本號、CVE ID |
| Preflight 缺項 (clasp, read:org) | 真實部署不可行 | 降級：本機模擬 + 明確標註 | 影片標註「本機模擬/未真實部署」 |

---

## 7. 已解決分歧 (尚無，待他人輸入)

---

## 8. Preflight 缺項與降級計畫

| 缺項 | 影響 | 降級方案 | 標註位置 |
|------|------|----------|----------|
| P2: clasp 未安裝/未登入 | Apps Script 無法真實部署 | 本機 Node 模擬 UrlFetch/Sheets 邏輯；代碼完整、可部署 | DONE.md、影片字幕、README |
| P1: gh 缺 `read:org` scope | 不影響公開 repo Pages | 無影響，繼續 | N/A |
| west 未安裝 | 已安裝 | N/A | N/A |

---

## 9. [UNVERIFIED] 清單 (待他人 Spike 驗證)

- [ ] Agent 1: `west spdx` 輸出轉 CycloneDX，PURL 保留情況、OSV 命中率
- [ ] Agent 2: 最小 Zephyr 建置在 GitHub Actions 耗時、快取效果
- [ ] Agent 3: 範例 CycloneDX 在 Apps Script 解析 + OSV querybatch 耗時、配額
- [ ] Agent 4: ffmpeg 重編 libass 成功、字幕燒錄對齊

---

## 10. 八大必答議題結論 (暫定，待他人確認)

| 議題 | 暫定結論 | 依據/備註 |
|------|----------|-----------|
| 1. Zephyr 元件在 OSV 比對結果與誠實呈現 | 改用「示範選例」+ 明確標示 | [MISSING: Agent 1 spike] |
| 2. VEX demo 策略與格式 | CycloneDX VEX 1.0；每判斷含 source_url | [MISSING: Agent 1 偏好] |
| 3. 範例 app、board、版本釘選 | `zephyr/samples/hello_world`, `qemu_x86`, Zephyr 3.6.0 | [MISSING: Agent 1 決定] |
| 4. Pages 是否需人類可讀頁面 | Should (Could) — 固定 URL 為 Must | Agent 4 建議 Could |
| 5. Apps Script secrets/scopes/配額 | PropertiesService + 最小 scopes + 配額記錄 | [MISSING: Agent 3 spike] |
| 6. 影片敘事與工具鏈 | 線性 + CVE 貫穿主線；ffmpeg + say + whisper.cpp | Agent 4 spike 驗證核心鏈路可行 |
| 7. Repo 結構與命名 | `orca-sbom-handoff/` 為 demo repo 名 | 統一前綴 |
| 8. 範圍取捨 | 見 §5 表格 | 依 Must/Should/Could |

---

## 下一步

等待 Agent 1–3 的 R0 提案與 spike 結果。收到後，Agent 4 將產出 PLAN_V2.md，納入他們輸入並解決分歧。