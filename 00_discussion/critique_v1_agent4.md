# Critique PLAN_V1 — Agent 4

## 未通過條目與具體修改建議

### C1 敘事 — 不通過
**問題**: 章節時長分配、旁白關鍵數值 (CVE ID、版本號、OSV 命中數) 全部為佔位符。無法確認 10–15 分鐘可行性。
**修改建議**: PLAN_V2 必須包含 Agent 1–3 確認的具體數值：Zephyr 版本、board、app、SBOM 組件數、OSV 命中數、VEX 判斷數、Actions 耗時、Apps Script 配額用量。Agent 4 擬定旁白草稿時直接引用這些數值。

### C2 資料誠實 — 不通過
**問題**: 所有 CVE、版本、數字標註 `[MISSING]`，無 spike 證據。OSV 命中率未知，無「命中率低時如實呈現」的具體做法 (例如：改用示範選例、明確標示、影片口頭說明)。
**修改建議**: 
1. Agent 1 spike 必須產出 `osv_hit_rate.md` 記錄：查詢 N 個 PURL，命中 M 個，命中率 M/N。
2. PLAN_V2 寫死：「若命中率 < 30%，影片改用 3 個真實 CVE 做示範選例，旁白/字幕標示『示範選例，非本 build 實際結果』」
3. 每個 CVE 在 VEX 與影片中必須附來源連結 (OSV/NVD/Zephyr advisory URL)

### C3 技術可行 — 不通過
**問題**: Agent 1–3 階段完全缺乏 spike 或官方文件證據。例如：`west spdx` 是否支援該 Zephyr 版本？CycloneDX 轉換工具哪個保留 PURL 完整？Apps Script 能否在 6 分鐘內處理 500+ 組件？
**修改建議**: 
- Agent 1: 提供 `west spdx` 實測 log、轉換工具對比表、OSV querybatch 實測回應
- Agent 2: 提供 Actions 實測 run 連結或 log 擷圖
- Agent 3: 提供本機 Node 模擬執行 log (含耗時、配額)
- PLAN_V2 每階段至少附 1 筆 `[EVIDENCE]` 連結

### C4 介面契約完整 — 不通過
**問題**: 契約為單方面定義，上游未確認。例如：Agent 1 可能產出 OpenVEX 而非 CycloneDX VEX；Agent 2 可能用不同 URL 結構；Agent 3 可能用不同 Sheet 結構。
**修改建議**: 
1. PLAN_V2 由 Agent 4 發起「契約確認」：在 SHARED 建立 `contracts/` 目錄，每個介面一個 JSON Schema + 範例檔
2. Agent 1–3 各自在對應 schema 下簽署 (建立 `contracts/signed_by_agent{N}.txt`)
3. 若有分歧，在 decisions.md 記錄並由領域負責人裁決

### C5 可重現 — 不通過
**問題**: 版本釘選、乾淨環境重現步驟皆待 Agent 1 定案。
**修改建議**: Agent 1 在 DONE.md 提供：`west init -m <manifest> --mr <rev>`, `west build -b <board>`, `west spdx` 完整指令序列，並附 `west --version`、Zephyr commit hash、SDK 版本。

### C6 Apps Script 可行與安全 — 不通過
**問題**: Scopes、配額、錯誤處理已草擬但無實測。單次執行時間、UrlFetch 配額、無資料庫/UI 限制皆為猜測。
**修改建議**: 
- Agent 3 spike 必須測：解析 100/500/1000 組件 CycloneDX 耗時、OSV querybatch 100/500 條耗時+配額、完整流程端到端耗時
- PLAN_V2 寫死具體數字：如「500 組件完整流程 4 分 12 秒，消耗 850 UrlFetch 配額」
- 錯誤處理細節：OSV 5xx 重試策略、網路超時、空回應、配額耗盡時行為

### C7 風險與備案 — 部分通過
**問題**: 僅含 Agent 4 視角風險，缺乏 Agent 1–3 的領域風險 (如：Zephyr 升級破壞 SBOM 格式、OSV API 變更、GitHub Pages 部署失敗模式)。
**修改建議**: PLAN_V2 的風險表需包含各 Agent 提供的前 3 大風險，共 12 項，去重後合併。

### C8 Gate 可客觀驗證 — 通過
**問題**: 無。每個 Gate 皆有具體指令/截圖驗證方式。

### C9 全自動可行 — 部分通過
**問題**: Preflight 缺項有降級計畫，但 Agent 1–3 階段未驗證是否真正全自動 (例如：west init 是否需互動、Actions 是否需手動 approve)。
**修改建議**: 各 Agent 在 DONE.md 明確列出「需人工操作的步驟」並給出降級方案。

### C10 討論紀錄完整 — 不通過
**問題**: 8 大議題有暫定結論，但無他人批評、無處置記錄、多項以 [GUESS] 為唯一依據。決定權歸屬未落實 (如 VEX 格式歸 Agent 1，但 Agent 1 未表態)。
**修改建議**: 
1. decisions.md 建立標準格式：議題、各方意見、spike 證據、裁決者、裁決理由、接受/部分接受/拒絕
2. 所有 [GUESS] 在 PLAN_V2 必須升級或移除
3. 缺席 Agent 的議題標註「缺席，由領域負責人單方面決定，待補齊」

---

## 給 Agent 1–3 的具體行動要求 (下一輪前)

| Agent | 必須在 PLAN_V2 前完成 | 輸出位置 |
|-------|----------------------|----------|
| 1 | R0 提案 + west spdx spike + OSV 命中率 + 版本/board/app 決定 | `R0_proposal_agent1.md`, `spikes/agent1_sbom_spike.md` |
| 2 | R0 提案 + Actions 耗時 spike + Pages URL 確認 | `R0_proposal_agent2.md`, `spikes/agent2_pages_spike.md` |
| 3 | R0 提案 + Apps Script 解析/查詢耗時 spike + 配額實測 | `R0_proposal_agent3.md`, `spikes/agent3_apps_spike.md` |

若 30 分鐘內仍無輸出，PLAN_V2 將記錄「缺席」並由我單方面推進，但在 decisions.md 明確標註風險。