FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建.env文件（在生产环境中应通过环境变量注入敏感信息）
RUN echo "DATABASE_URL=postgresql://admin:password@db:5432/example_db" > .env && \
    echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env && \
    echo "DEBUG=False" >> .env

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]