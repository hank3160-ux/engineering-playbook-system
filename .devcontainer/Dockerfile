FROM python:3.11-slim

# 安裝系統工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安裝開發工具
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn[standard]==0.29.0 \
    pydantic==2.6.4 \
    pydantic-settings==2.2.1 \
    sqlalchemy[asyncio]==2.0.29 \
    asyncpg==0.29.0 \
    aiosqlite==0.20.0 \
    pytest==8.1.1 \
    pytest-asyncio==0.23.6 \
    httpx==0.27.0 \
    ruff==0.4.1 \
    mypy==1.9.0

WORKDIR /workspace
