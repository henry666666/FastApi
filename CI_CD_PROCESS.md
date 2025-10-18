# CI/CD 流程文档

本文档详细说明如何使用 Docker Compose 为 FastAPI 应用实现 CI/CD 流程。

## 目录结构

```
fastApi/
├── Dockerfile              # 应用容器构建文件
├── docker-compose.yml      # 多服务编排配置
├── start_services.sh       # 服务管理脚本
├── nginx/
│   ├── conf.d/             # Nginx 配置目录
│   └── certs/              # SSL 证书目录
└── CI_CD_PROCESS.md        # 本 CI/CD 流程文档
```

## 环境要求

- Docker (19.03+) 
- Docker Compose (1.25+)
- Git (版本控制)

## 服务组件

我们的 Docker Compose 配置包含以下服务：

1. **app**: FastAPI 应用服务
2. **db**: PostgreSQL 数据库服务
3. **migration**: 数据库迁移服务 (可选)
4. **nginx**: Nginx 反向代理服务 (可选，用于生产环境)

## CI/CD 流程步骤

### 1. 开发环境设置

1. 克隆代码库
   ```bash
   git clone <repository-url>
   cd fastApi
   ```

2. 创建 `.env` 文件（开发环境）
   ```bash
   cp .env.example .env
   ```
   编辑 `.env` 文件，设置数据库连接信息和密钥

3. 使用 Docker Compose 启动开发环境
   ```bash
   docker-compose up --build
   ```

### 2. 构建和测试（CI）

1. 构建 Docker 镜像
   ```bash
   docker-compose build
   ```

2. 运行测试
   ```bash
   docker-compose run app python -m pytest
   ```

### 3. 部署流程（CD）

#### 开发环境部署

```bash
./start_services.sh --build
```

#### 生产环境部署

1. 准备生产环境配置
   - 修改 `.env` 文件，设置 `DEBUG=False`
   - 配置 Nginx SSL 证书（可选）

2. 构建并启动生产环境服务
   ```bash
   docker-compose -f docker-compose.yml up --build -d
   ```

3. 数据库迁移（如果使用 alembic）
   ```bash
   docker-compose run migration
   ```

## 自动化 CI/CD 配置示例

### GitHub Actions 配置示例

创建文件：`.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      - name: Build and test
        run: |
          docker-compose build
          docker-compose run app python -m pytest

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /path/to/app
            git pull origin ${{ github.ref_name }}
            ./start_services.sh --build --detach
```

### GitLab CI/CD 配置示例

创建文件：`.gitlab-ci.yml`

```yaml
stages:
  - test
  - deploy

test:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - apk add --no-cache docker-compose
    - docker-compose build
    - docker-compose run app python -m pytest

variables:
  DOCKER_HOST: tcp://docker:2375/
  DOCKER_TLS_CERTDIR: ""

deploy_production:
  stage: deploy
  only:
    - main
  script:
    - echo "部署到生产环境"
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_HOST "cd /path/to/app && git pull && ./start_services.sh --build --detach"

variables:
  SERVER_HOST: ${{ secrets.SERVER_HOST }}
  SERVER_USER: ${{ secrets.SERVER_USER }}
```

## 服务管理命令

我们提供了便捷的 `start_services.sh` 脚本来管理服务：

```bash
# 构建并启动服务
./start_services.sh --build

# 后台模式启动服务
./start_services.sh --detach

# 停止所有服务
./start_services.sh --stop

# 重启服务
./start_services.sh --restart

# 查看服务日志
./start_services.sh --logs
```

## 环境变量配置

### 必要环境变量

| 环境变量 | 描述 | 默认值 |
|---------|------|-------|
| DATABASE_URL | 数据库连接 URL | postgresql://admin:password@db:5432/example_db |
| SECRET_KEY | JWT 密钥 | your-secret-key-here |
| DEBUG | 调试模式开关 | False |

### 数据库配置

| 环境变量 | 描述 | 默认值 |
|---------|------|-------|
| POSTGRES_USER | PostgreSQL 用户名 | admin |
| POSTGRES_PASSWORD | PostgreSQL 密码 | password |
| POSTGRES_DB | PostgreSQL 数据库名 | example_db |

## 安全最佳实践

1. **环境变量管理**
   - 在生产环境中，不要将敏感信息（如密码、密钥）硬编码在代码中
   - 使用环境变量或密钥管理服务

2. **容器安全**
   - 使用非 root 用户运行应用容器
   - 定期更新基础镜像和依赖
   - 使用最小化的基础镜像（如 alpine）

3. **数据库安全**
   - 使用强密码
   - 限制数据库访问权限
   - 生产环境中启用 SSL

4. **网络安全**
   - 使用私有网络
   - 生产环境中配置 SSL
   - 限制暴露的端口

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否正常运行：`docker-compose ps db`
   - 验证数据库凭证是否正确
   - 检查网络连接：`docker-compose logs app`

2. **应用启动失败**
   - 查看应用日志：`docker-compose logs app`
   - 检查依赖安装：`docker-compose exec app pip list`
   - 验证环境变量：`docker-compose exec app env`

3. **Nginx 配置问题**
   - 检查 Nginx 配置：`docker-compose exec nginx nginx -t`
   - 查看 Nginx 日志：`docker-compose logs nginx`

## 扩展与优化

1. **水平扩展**
   - 使用 `docker-compose up --scale app=3` 扩展应用实例
   - 考虑使用负载均衡器

2. **数据备份**
   - 定期备份数据库：`docker-compose exec db pg_dump -U admin example_db > backup.sql`
   - 配置自动备份策略

3. **监控与日志**
   - 集成 Prometheus 和 Grafana 进行监控
   - 配置 ELK 或 Graylog 收集日志

4. **持续优化**
   - 使用多阶段构建减小镜像大小
   - 配置 Docker 缓存提高构建速度
   - 定期进行性能测试和优化