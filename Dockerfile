# ---- 阶段1：构建前端（frontend/ 未就绪时自动回退占位页）----
FROM node:20-alpine AS web
WORKDIR /ctx
COPY . .
RUN if [ -f frontend/package.json ]; then \
      cd frontend && npm ci && npm run build && mkdir -p /build/dist && cp -r dist/. /build/dist/; \
    else mkdir -p /build/dist && cp backend/static/index.html /build/dist/index.html; \
    fi

# ---- 阶段2：运行镜像（前端+后端同容器）----
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=web /build/dist ./static
RUN useradd -m app && mkdir -p /app/data && chown -R app /app
# 非 root 运行
USER app
ENV DB_PATH=/app/data/app.db
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
