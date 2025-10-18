# 订单管理系统 (FastAPI版本)

## 项目简介

本项目是一个订单管理系统，由Spring Boot迁移至FastAPI框架实现。系统提供用户认证与授权、商家管理、商品管理和订单管理等核心功能，采用现代化的Python异步Web框架构建，具备高性能和良好的开发体验。

项目采用了现代Python后端开发架构：
- **FastAPI** 作为Web框架
- **SQLAlchemy** 作为ORM
- **Docker** 用于容器化部署
- **SQLite** 作为数据库
- **JWT** 用于身份认证

## 项目文档体系

为方便新接触项目的开发人员快速了解项目结构和重要文档内容，以下是项目文档列表及简要说明：

1. **[README.md](README.md)**
   **项目主文档**，包含项目概述、快速开始指南、基本使用说明等核心信息。

2. **[TEST_RESULTS_SUMMARY.md](TEST_RESULTS_SUMMARY.md)**
   **测试结果摘要**，记录了API测试的详细结果，包括测试用例执行情况、问题诊断与修复过程等。

3. **[CI_CD_PROCESS.md](CI_CD_PROCESS.md)**
   **CI/CD流程文档**，详细说明如何使用Docker Compose为FastAPI应用实现CI/CD流程。

4. **[SIMPLE_API_TESTING_PLAN.md](SIMPLE_API_TESTING_PLAN.md)**
   **简单API测试计划**，定义了项目API的基础测试策略、测试场景和测试方法。

5. **[STABILITY_TESTING_PLAN.md](STABILITY_TESTING_PLAN.md)**
   **稳定性测试计划**，专注于系统稳定性和性能测试的策略和方法。

6. **[API_RESPONSE_OPTIMIZATION.md](API_RESPONSE_OPTIMIZATION.md)**
   **API响应优化指南**，提供了优化API响应性能和质量的建议和方法。

7. **[API_TESTING.md](API_TESTING.md)**
   **API测试详细文档**，包含API测试的完整方法、工具使用和最佳实践。

8. **[MIGRATION_PROCESS.md](MIGRATION_PROCESS.md)**
   **数据库迁移流程**，描述了数据库结构变更和数据迁移的规范和步骤。

9. **[PROJECT_MAPPING.md](PROJECT_MAPPING.md)**
   **项目映射文档**，展示了项目各组件之间的关系和模块映射。

10. **[TASK.md](TASK.md)**
    **任务描述文档**，记录了项目的具体任务、要求和实现细节。

## 推荐阅读顺序

对于新接触项目的开发人员，建议按以下顺序阅读文档：

1. 先阅读本README.md了解项目基本情况
2. 查看[TEST_RESULTS_SUMMARY.md](TEST_RESULTS_SUMMARY.md)了解API功能和测试情况
3. 阅读[CI_CD_PROCESS.md](CI_CD_PROCESS.md)了解如何部署和运行项目
4. 根据需要深入阅读其他专业文档

## 项目架构

项目采用经典的分层架构设计，包括：

1. **数据模型层 (Model)**：使用SQLAlchemy定义数据模型
2. **数据访问层 (Repository)**：负责数据库操作
3. **业务逻辑层 (Service)**：实现核心业务逻辑
4. **API路由层 (Router)**：提供HTTP接口
5. **工具层 (Utils)**：包含各种工具函数
6. **异常处理层**：统一处理各类异常

## 项目结构

```
fastApi/
├── app.py                  # 应用主入口
├── config.py               # 配置文件
├── database.py             # 数据库配置
├── models.py               # 数据模型定义
├── exceptions.py           # 自定义异常类
├── exception_handler.py    # 全局异常处理器
├── repository/             # 数据访问层
│   ├── __init__.py
│   ├── user_repository.py
│   ├── merchant_repository.py
│   ├── product_repository.py
│   ├── order_repository.py
│   └── order_item_repository.py
├── service/                # 业务逻辑层
│   ├── __init__.py
│   ├── user_service.py
│   ├── merchant_service.py
│   ├── product_service.py
│   └── order_service.py
├── routers/                # API路由层
│   ├── __init__.py
│   ├── user.py
│   ├── merchant.py
│   ├── product.py
│   └── order.py
├── utils/                  # 工具层
│   ├── __init__.py
│   ├── password_util.py
│   └── validation_util.py
├── requirements.txt        # 项目依赖
└── order_management.db     # SQLite数据库文件
```

## 核心功能

1. **用户管理**
   - 用户注册、登录
   - 用户信息查询和更新
   - 基于JWT的身份认证

2. **商家管理**
   - 商家信息的增删改查
   - 商家状态管理

3. **产品管理**
   - 产品信息的增删改查
   - 产品库存管理
   - 产品状态管理

4. **订单管理**
   - 创建订单
   - 查询订单信息
   - 更新订单状态
   - 订单明细管理

## 技术栈

- **Web框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite
- **认证**: JWT (JSON Web Tokens)
- **密码加密**: bcrypt
- **数据验证**: Pydantic
- **服务器**: Uvicorn

## 快速开始

### 环境要求
- Docker Desktop (Windows/macOS) 或 Docker + Docker Compose (Linux)
- Python 3.11+（如直接在本地运行）

### 使用Docker运行项目

```bash
# Windows系统
start_services.bat --build

# Linux/macOS系统
./start_services.sh --build
```

### 使用Python直接运行

#### 1. 环境准备

确保已安装Python 3.8或更高版本，然后进入项目目录：

```bash
cd c:/Users/Administrator/Desktop/testdemo/java-demo/fastApi
```

#### 2. 安装依赖

使用pip安装项目所需的所有依赖：

```bash
pip install -r requirements.txt
```

#### 3. 数据库初始化

项目使用SQLite数据库，数据库文件会在首次运行时自动创建，无需额外配置。

#### 4. 启动应用

使用以下命令启动FastAPI应用：

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

- `--host 0.0.0.0`: 允许从任何IP地址访问
- `--port 8000`: 使用8000端口
- `--reload`: 启用热重载，修改代码后自动重启服务

### 运行测试

```bash
# Windows系统
start_services.bat --test

# Linux/macOS系统
docker-compose run app python -m pytest

# 直接使用Python运行
python -m pytest
```

### 访问API文档

应用启动后，可以通过以下地址访问自动生成的API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 停止服务

按 `Ctrl + C` 停止运行中的服务（如果直接使用Python运行）

## API使用说明

### 认证

大部分API需要JWT认证，认证流程如下：

1. 调用登录接口获取token
2. 在后续请求的Authorization头中添加token：`Bearer {your_token}`

### 主要API端点

- **用户相关**
  - POST `/api/users/register` - 用户注册
  - POST `/api/users/login` - 用户登录
  - GET `/api/users/me` - 获取当前用户信息

- **商家相关**
  - GET `/api/merchants` - 获取商家列表
  - POST `/api/merchants` - 创建新商家
  - GET `/api/merchants/{id}` - 获取商家详情
  - PUT `/api/merchants/{id}` - 更新商家信息
  - DELETE `/api/merchants/{id}` - 删除商家

- **产品相关**
  - GET `/api/products` - 获取产品列表
  - POST `/api/products` - 创建新产品
  - GET `/api/products/{id}` - 获取产品详情
  - PUT `/api/products/{id}` - 更新产品信息
  - DELETE `/api/products/{id}` - 删除产品

- **订单相关**
  - GET `/api/orders` - 获取订单列表
  - POST `/api/orders` - 创建新订单
  - GET `/api/orders/{id}` - 获取订单详情
  - PUT `/api/orders/{id}/status` - 更新订单状态

## 开发说明

### 代码风格

- 遵循Python PEP 8规范
- 使用类型注解增强代码可读性
- 添加适当的注释说明复杂逻辑

### 调试技巧

- 使用`--reload`参数启动开发服务器，修改代码后自动重启
- 利用FastAPI的交互式文档进行API测试
- 使用Python内置的pdb模块进行代码调试

## 迁移检查清单

- [ ] 设置FastAPI项目结构
- [ ] 实现SQLAlchemy模型
- [ ] 创建Pydantic模型
- [ ] 移植核心业务逻辑
- [ ] 实现API端点
- [ ] 添加认证功能
- [ ] 设置数据库迁移
- [ ] 编写单元测试
- [ ] 配置部署

请查看`TASK.MD`了解详细的实施任务和进度跟踪。

## 许可证

© 2023 订单管理系统。保留所有权利。

本项目仅作为学习和演示用途，未经授权不得用于商业目的。您可以自由修改和学习本项目的代码，但请在使用时注明原作者和来源。
