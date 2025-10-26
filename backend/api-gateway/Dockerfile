FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 设置 Python 路径，使 shared 模块可以被导入
ENV PYTHONPATH=/app:/app/shared

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
