# -------------------------------------------------------
# Multi-stage build — 最小化正式映像體積
# -------------------------------------------------------

# Stage 1: builder — 安裝依賴
FROM python:3.11-slim AS builder

WORKDIR /build

COPY demo/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: runtime — 只複製必要檔案
FROM python:3.11-slim AS runtime

# 建立非 root 使用者，降低攻擊面
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# 從 builder 複製已安裝的套件
COPY --from=builder /install /usr/local

# 複製應用程式原始碼
COPY demo/ ./demo/

# 切換至非 root 使用者
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "demo.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
