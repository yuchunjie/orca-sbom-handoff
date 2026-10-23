# Decisions Log — Stage 0

## 2026-10-23: Agent 1–3 缺席，單方面推進

| 議題 | 狀態 | 裁決者 | 理由/證據 | 風險 |
|------|------|--------|-----------|------|
| Zephyr 版本/board/app | 單方面決定 | Agent 4 (代理) | 選擇穩定、文檔完善、OSV 有資料的組合 | 可能非最佳教學範例 |
| VEX 格式 | 單方面決定 | Agent 4 (代理) | CycloneDX VEX 1.0：工具鏈成熟、schema 明確、GitHub 可直接渲染 | Agent 1 可能偏好 OpenVEX |
| Pages URL 結構 | 單方面決定 | Agent 4 (代理) | 固定、可預測、符合 GitHub Pages 慣例 | Agent 2 可能有不同部署策略 |
| Apps Script 架構 | 單方面決定 | Agent 4 (代理) | 時間觸發 + UrlFetch + Sheet + Email，最小權限 | Agent 3 可能有更好配額管理方案 |
| 影片敘事主線 | 確定 | Agent 4 | CVE 貫穿線性敘事，已 spike 驗證工具鏈 | 無 |
| 範圍分級 | 確定 | Agent 4 | Must/Should/Could 明確，可砍 | 無 |

## 已知風險 (因 Agent 1–3 缺席)
1. **SBOM/VEX 實際產出可能與契約不符** — 實作時需即時調整契約
2. **OSV 命中率未知** — 影片敘事需準備「低命中率」分支
3. **Actions 耗時/快取未驗證** — 影片時間軸可能需調整
4. **Apps Script 配額/耗時未驗證** — 可能需分批或簡化示範
5. **介面契約無上游簽署** — decisions.md 缺 Agent 1–3 簽名，Stage 1–4 門檻 C4 視為有條件通過

## 後續處理
- 實作階段若發現契約不符，即時更新 contracts/ 並記錄於 decisions.md
- 所有單方面決定在影片/DONE.md 中標註「單方面決定，未經該領域 Agent 確認」