## 變更摘要

> 簡短說明這個 PR 做了什麼，以及為什麼需要這個變更。

Closes #<!-- issue number -->

---

## 變更類型

- [ ] `feat` — 新功能
- [ ] `fix` — Bug 修復
- [ ] `docs` — 文件更新
- [ ] `refactor` — 重構（不影響功能）
- [ ] `test` — 測試新增或修改
- [ ] `chore` — 建置工具、依賴更新
- [ ] `ci` — CI/CD 設定變更

---

## 測試

- [ ] 已在本地執行 `pytest demo/tests/ -v`，所有測試通過
- [ ] 新功能已加入對應測試
- [ ] 若涉及 API 變更，已手動驗證 `/health` 或相關端點

---

## 文件

- [ ] 相關 `playbook/` 文件已同步更新
- [ ] `README.md` 若有結構變更已更新
- [ ] `.env.example` 若有新環境變數已更新

---

## 代碼規範

- [ ] 已執行 `ruff check .`，無 linting 錯誤
- [ ] 已執行 `bash scripts/check-secrets.sh`，無敏感資料洩露
- [ ] Commit message 符合 Conventional Commits 規範
- [ ] 無 hardcoded credentials 或 debug 用的 `print()`

---

## 截圖 / 補充說明

<!-- 如有 UI 變更或需要額外說明，請在此附上截圖或說明 -->
