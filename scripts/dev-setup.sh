#!/usr/bin/env bash
# -------------------------------------------------------
# dev-setup.sh — 開發環境一鍵初始化腳本
#
# 執行內容：
#   1. 建立 Python 虛擬環境
#   2. 安裝所有依賴（含開發工具）
#   3. 安裝 pre-commit hooks
#   4. 複製 .env.example → .env（若不存在）
#   5. 執行測試預熱，確認環境正常
#
# 用法：bash scripts/dev-setup.sh
# -------------------------------------------------------

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

step() { echo -e "\n${GREEN}▶ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; exit 1; }

# -------------------------------------------------------
# 1. Python 版本檢查
# -------------------------------------------------------
step "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED="3.11"

if ! python3 -c "import sys; assert sys.version_info >= (3,11)" 2>/dev/null; then
    fail "Python $REQUIRED+ required, found $PYTHON_VERSION"
fi
echo "  Python $PYTHON_VERSION ✓"

# -------------------------------------------------------
# 2. 虛擬環境
# -------------------------------------------------------
step "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "  Created .venv"
else
    warn ".venv already exists, skipping creation"
fi

# shellcheck disable=SC1091
source .venv/bin/activate

# -------------------------------------------------------
# 3. 安裝依賴
# -------------------------------------------------------
step "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r demo/requirements.txt
pip install --quiet \
    pytest==8.1.1 \
    pytest-asyncio==0.23.6 \
    httpx==0.27.0 \
    aiosqlite==0.20.0 \
    ruff==0.4.1 \
    mypy==1.9.0 \
    pre-commit==3.7.0 \
    pydantic-settings==2.2.1
echo "  All dependencies installed ✓"

# -------------------------------------------------------
# 4. Pre-commit hooks
# -------------------------------------------------------
step "Installing pre-commit hooks..."
pre-commit install
echo "  Pre-commit hooks installed ✓"

# -------------------------------------------------------
# 5. 環境變數檔案
# -------------------------------------------------------
step "Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f "template/.env.example" ]; then
        cp template/.env.example .env
        echo "  Copied template/.env.example → .env"
        warn "Please edit .env and fill in actual values before running the service"
    else
        warn "No .env.example found, skipping"
    fi
else
    warn ".env already exists, skipping"
fi

# -------------------------------------------------------
# 6. 測試預熱
# -------------------------------------------------------
step "Running test suite to verify environment..."
if pytest demo/tests/ -v --tb=short -q 2>&1; then
    echo -e "\n${GREEN}✅ All tests passed — environment is ready!${NC}"
else
    fail "Tests failed. Please check the output above."
fi

# -------------------------------------------------------
# 完成
# -------------------------------------------------------
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Dev environment ready. Next steps:${NC}"
echo -e "${GREEN}  1. source .venv/bin/activate${NC}"
echo -e "${GREEN}  2. uvicorn demo.main:app --reload${NC}"
echo -e "${GREEN}  3. curl -i http://localhost:8000/health${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
