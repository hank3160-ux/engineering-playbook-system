#!/usr/bin/env bash
# -------------------------------------------------------
# check-secrets.sh — Pre-commit 敏感資料掃描腳本
#
# 用法：
#   手動執行：bash scripts/check-secrets.sh
#   Git hook：複製至 .git/hooks/pre-commit 並 chmod +x
#
# 偵測目標：明文密碼、API key、token、私鑰等常見洩露模式
# -------------------------------------------------------

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FOUND=0

# 取得即將 commit 的檔案清單（排除已刪除的）
if git rev-parse --verify HEAD > /dev/null 2>&1; then
    FILES=$(git diff --cached --name-only --diff-filter=ACM)
else
    # 首次 commit，掃描所有 staged 檔案
    FILES=$(git diff --cached --name-only --diff-filter=ACM)
fi

if [ -z "$FILES" ]; then
    echo -e "${GREEN}[check-secrets] No staged files to scan.${NC}"
    exit 0
fi

echo "🔍 Scanning staged files for secrets..."

# -------------------------------------------------------
# 掃描規則：pattern | 說明
# -------------------------------------------------------
declare -A PATTERNS=(
    ["password\s*=\s*['\"][^'\"]{4,}['\"]"]="Hardcoded password"
    ["secret\s*=\s*['\"][^'\"]{4,}['\"]"]="Hardcoded secret"
    ["api_key\s*=\s*['\"][^'\"]{8,}['\"]"]="Hardcoded API key"
    ["token\s*=\s*['\"][^'\"]{8,}['\"]"]="Hardcoded token"
    ["-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"]="Private key"
    ["AKIA[0-9A-Z]{16}"]="AWS Access Key ID"
    ["ghp_[0-9a-zA-Z]{36}"]="GitHub Personal Access Token"
    ["sk-[a-zA-Z0-9]{32,}"]="OpenAI API Key"
)

for FILE in $FILES; do
    # 跳過二進位檔、.env.example、本腳本自身
    [[ "$FILE" == *.png ]] && continue
    [[ "$FILE" == *.jpg ]] && continue
    [[ "$FILE" == *.gif ]] && continue
    [[ "$FILE" == *.pdf ]] && continue
    [[ "$FILE" == *".env.example" ]] && continue
    [[ "$FILE" == "scripts/check-secrets.sh" ]] && continue

    for PATTERN in "${!PATTERNS[@]}"; do
        DESC="${PATTERNS[$PATTERN]}"
        # 在 staged 內容中搜尋（不掃描工作目錄）
        MATCHES=$(git show ":$FILE" 2>/dev/null | grep -inE "$PATTERN" || true)
        if [ -n "$MATCHES" ]; then
            echo -e "${RED}[FAIL] ${DESC} detected in: ${FILE}${NC}"
            echo "$MATCHES" | head -3
            FOUND=1
        fi
    done
done

if [ "$FOUND" -eq 1 ]; then
    echo ""
    echo -e "${RED}❌ Secret scan FAILED. Commit aborted.${NC}"
    echo -e "${YELLOW}   請移除敏感資料後重新 commit。${NC}"
    echo -e "${YELLOW}   若為誤判，可使用 git commit --no-verify 跳過（需主管核准）。${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Secret scan passed. No secrets detected.${NC}"
    exit 0
fi
